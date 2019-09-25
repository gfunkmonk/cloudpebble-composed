""" These are integration tests which just exist to help with development. They are not particularly exhaustive are not
run automatically.
The dependencies test relies on the the git repo Katharine/pebble-events existing. """
from __future__ import print_function

import unittest
import subprocess

from ycm_helpers import spinup, kill_completers, get_completions

SIMPLE_CONTENT = """
#include <pebble.h>

int main(void) {
  APP_LOG(APP_LOG_LEVEL_DEBUG, "Hello World!");
  APP
}
"""

LIBRARIES_CONTENT = """
#include <pebble.h>
#include "{include}"

int main(void) {{
  APP_LOG(APP_LOG_LEVEL_DEBUG, "Hello world");
  {text}
}}
"""


class TestYCM(unittest.TestCase):
    def tearDown(self):
        kill_completers()

    def spinup(self, options):
        options['sdk'] = options.get('sdk', '3')
        result = spinup(options)
        self.assertTrue(result['success'])
        return result['uuid']

    def expect_completion(self, uuid, line, ch, expect, filename='main.c'):
        self.assertIn(expect, [x['insertion_text'] for x in get_completions(uuid, {
            'file': filename,
            'line': line,
            'ch': ch
        })['completions']])

    def test_spinup(self):
        """ Check that spinup and a completion of 'APP_LOG' works """
        uuid = self.spinup({'files': {'main.c': SIMPLE_CONTENT}})
        self.expect_completion(uuid, 5, 6, 'APP_LOG')

    def test_dependencies(self):
        """ Check that YCM can autocomplete on external libraries. """
        try:
            uuid = self.spinup({
                'files': {'main.c': LIBRARIES_CONTENT.format(include="pebble-events/pebble-events.h", text="even")},
                'dependencies': {'pebble-events': '^1.0.0'}
            })
        except subprocess.CalledProcessError as e:
            print(e.output)
            raise
        self.expect_completion(uuid, 6, 6, 'events_health_service_events_unsubscribe')

    def test_namespaced_dependencies(self):
        """ Check that YCM can autocomplete on namespaced external libraries. """
        try:
            uuid = self.spinup({
                'files': {'main.c': LIBRARIES_CONTENT.format(include="@smallstoneapps/linked-list/linked-list.h", text="linked_lis")},
                'dependencies': {'@smallstoneapps/linked-list': "^1.2.1"}
            })
        except subprocess.CalledProcessError as e:
            print(e.output)
            raise
        self.expect_completion(uuid, 6, 12, 'linked_list_insert')

    def test_bad_dependency(self):
        """ Check that YCM fails to spinup if unsafe dependencies are specified. """
        with self.assertRaises(ValueError):
            self.spinup({
                'files': {'main.c': LIBRARIES_CONTENT},
                'dependencies': {'libname': '../local/file'}
            })
