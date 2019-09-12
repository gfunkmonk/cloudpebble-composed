#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import gevent.monkey; gevent.monkey.patch_all(subprocess=True)
from flask import Flask, request, jsonify

from flask_cors import CORS
import atexit
import gevent
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import geventwebsocket
import ssl
import json
import signal
import traceback
import os
import pwd
import grp
from . import settings
from . import ycm_helpers

app = Flask(__name__)

cors = CORS(app, headers=["X-Requested-With", "X-CSRFToken", "Content-Type"], resources="/ycm/*")


@app.route('/spinup', methods=['POST'])
def spinup():
    content = request.get_json(force=True)
    result = ycm_helpers.spinup(content)
    result['ws_port'] = settings.PORT
    result['secure'] = (settings.SSL_ROOT is not None)
    return jsonify(result)


def server_ws(process_uuid):
    ws_commands = {
        'completions': ycm_helpers.get_completions,
        'errors': ycm_helpers.get_errors,
        'goto': ycm_helpers.go_to,
        'create': ycm_helpers.create_file,
        'delete': ycm_helpers.delete_file,
        'rename': ycm_helpers.rename_file,
        'resources': ycm_helpers.update_resources,
        'messagekeys': ycm_helpers.update_messagekeys,
        'dependencies': ycm_helpers.update_dependencies,
        'ping': ycm_helpers.ping
    }

    # Get the WebSocket from the request context
    socket = request.environ.get('wsgi.websocket', None)
    if socket is None:
        return "websocket endpoint", 400

    # Functions to send back a response to a message, with its message ID.
    def respond(message_id, response, success=True):
        key = 'data' if success else 'error'
        return socket.send(json.dumps({
            key: response,
            '_id': message_id,
            'success': success
        }))

    # Loop for as long as the WebSocket remains open
    try:
        while True:
            raw = socket.receive()
            packet_id = None
            if raw is None:
                continue

            try:
                packet = json.loads(raw)
                packet_id = packet['_id']
                command = packet['command']
                data = packet['data']
            except (KeyError, ValueError):
                respond(packet_id, 'invalid packet', success=False)
                continue

            if command not in ws_commands:
                respond(packet_id, 'unknown command', success=False)
                continue

            # Run the specified command with the correct uuid and data
            try:
                print("Running command: %s" % command)
                ycms = ycm_helpers.get_ycms(process_uuid)
                result = ws_commands[command](ycms, data)
            except ycm_helpers.YCMProxyException as e:
                respond(packet_id, e.message, success=False)
                continue
            except Exception as e:
                traceback.print_exc()
                respond(packet_id, e.message, success=False)
                continue

            respond(packet_id, result, success=True)
    except (geventwebsocket.WebSocketError, TypeError):
        # WebSocket closed
        pass
    finally:
        ycm_helpers.kill_completer(process_uuid)

    print("Closing websocket")

    return ''


@app.route('/ycm/<process_uuid>/ws')
def ycm_ws(process_uuid):
    return server_ws(process_uuid)


@atexit.register
def kill_completers():
    print("Shutting down completers")
    ycm_helpers.kill_completers()


def drop_privileges(uid_name='nobody', gid_name='nogroup'):
    if os.getuid() != 0:
        # We're not root so, like, whatever dude
        return

    # Get the uid/gid from the name
    running_uid = pwd.getpwnam(uid_name).pw_uid
    running_gid = grp.getgrnam(gid_name).gr_gid

    # Remove group privileges
    os.setgroups([])

    # Try setting the new uid/gid
    os.setgid(running_gid)
    os.setuid(running_uid)

    # Ensure a very conservative umask
    os.umask(0o77)


def run_server():
    app.debug = settings.DEBUG

    ycm_helpers.monitor_processes()

    ssl_args = {}
    if settings.SSL_ROOT is not None:
        print("Running with SSL")
        ssl_args = {
            'keyfile': os.path.join(settings.SSL_ROOT, 'server-key.pem'),
            'certfile': os.path.join(settings.SSL_ROOT, 'server-cert.pem'),
            'ca_certs': os.path.join(settings.SSL_ROOT, 'ca-cert.pem'),
            'ssl_version': ssl.PROTOCOL_TLSv1,
        }
    server = pywsgi.WSGIServer(('', settings.PORT), app, handler_class=WebSocketHandler, **ssl_args)

    # Ensure that the program actually quits when we ask it to
    def sigterm_handler(_signo, _stack_frame):
        server.stop(timeout=1)
    signal.signal(signal.SIGTERM, sigterm_handler)

    server.start()
    if settings.RUN_AS_USER is not None:
        drop_privileges(settings.RUN_AS_USER, settings.RUN_AS_USER)
    server.serve_forever()


if __name__ == '__main__':
    run_server()
