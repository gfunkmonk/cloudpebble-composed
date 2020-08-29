# cloudpebble-composed
Local development setup for CloudPebble
https://developer.rebble.io/developer.pebble.com/guides/tools-and-resources/cloudpebble/index.html
====================

This repo contains the key components of CloudPebble as submodules. It also contains a
`docker-compose` file that will assemble all of them into something that runs like a
real CloudPebble instance.

Getting Started
---------------

1. Install [Docker Toolbox](https://www.docker.com/docker-toolbox) (Mac, Windows),
   or otherwise get docker and docker-compose into a working state (Linux).
2. Enter a shell with docker set up appropriately (e.g. via "Docker Quickstart Terminal")
3. `git clone https://github.com/gfunkmonk/cloudpebble-composed.git && cd cloudpebble-composed`
4. `./dev_setup.sh` (this will take a while)
5. `docker-compose up`

At the end of this, you will have seven Docker containers running. The CloudPebble-specific ones
should pick up most changes without being rebuilt, although in some cases you may have to stop and
restart them (re-run `docker-compose up`).

The current compose file assumes that the docker machine/VM is accessible at 192.168.99.100. This
is true by default, but may not be true for you.

Limitations
-----------

- Websocket installs are not available (working on)
- Emulator randomly crashes
Future Plans:
-------------

- Replace bower with yarn or nodejs or anything...
- update django to at least 1.9. (there's and old branch in 
  pebbles github..)
- Attempt to get the websocket phone connection working.
- Fix more of the security risks from outdated packages and 
  impliment HTTPS/SSL
- Maybe update the emulator/port/patch/hack n pray to a newer
  version of qemu.
