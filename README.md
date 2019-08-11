Cloudpebble Composed
====================

Cloudpebble is from https://github.com/pebble/cloudpebble-composed

Notes:
------
RockyJS doesn't seem to work.

Developer Websocket isn't available

The Pebble SDK is loaded from https://github.com/aveao/PebbleArchive/tree/master/SDKCores where SDK2 isn't available, so for SDK2 buillds, the oldest SDK3 is used which may not function the same.

Changes:
--------
Changed node signatures that prevented web from building.

removed analytics (local and google based).

updated sdk sources.

loaded pypkjs from folder not git, with small one line change to fix "GreenletExit".

serve fonts locally, obtained from https://www.profont.net/family/pf-din-display-pro.html




This repo contains the key components of CloudPebble as submodules. It also contains a
`docker-compose` file that will assemble all of them into something that runs like a
real CloudPebble instance.

Getting Started
---------------

1. Install docker and docker-compose (for linux, also "sudo apt install docker-compose -y")
 
    SEE: https://docs.docker.com/install/linux/docker-ce/ubuntu/.
    OR: https://docs.docker.com/docker-for-windows/install/.

2. Enter a shell with docker set up appropriately (e.g. via "Docker Quickstart Terminal") (remember to setup ssh keys)
3. `git clone --recursive git@github.com:pebble/cloudpebble-composed.git && cd cloudpebble-composed`
4. `./dev_setup.sh` (this will take a while)
5. `docker-compose up`

At the end of this, you will have seven Docker containers running. The CloudPebble-specific ones
should pick up most changes without being rebuilt, although in some cases you may have to stop and
restart them (re-run `docker-compose up`).

The current compose file assumes that the docker machine/VM is accessible at 192.168.99.100. This
is true by default, but may not be true for you.

Limitations
-----------

- Pebble SSO is not available; only local accounts work.
- Websocket installs are not available because pebble SSO is not available
- You'll have to change things manually if 192.168.99.100 isn't right.
