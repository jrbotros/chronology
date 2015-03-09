#Deploying with Docker

## Quick usage HOWTO

We've already pushed a working [Dockerfile to Docker Hub](https://registry.hub.docker.com/u/chronology/kronos/), so you can do something like the following:

  * Put a `settings.py` in `/etc/kronos/settings.py`
  * Create `/var/log/kronos` for log output
  * Run `sudo docker run -d -p 8150:8150 -v /etc/kronos:/etc/kronos -v /var/log/kronos:/var/log/kronos chronology/kronos:$(KRONOS_VERSION)`

## How to build/push future versions

  * `./build.sh [git hash or tag you want to build] chronology/kronos:v[version]`
  * `python ../../docker_tools/manage_docker.py push --tag chronology/kronos:v[version]`

Note: Docker aggressively caches commands for performance.  To avoid this, in build.sh, add --no-cache option to `manage_docker.py build.`