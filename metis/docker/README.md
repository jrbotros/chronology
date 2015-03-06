#Deploying with Docker

## Quick usage HOWTO

We've already pushed a working [Dockerfile to Docker Hub](https://registry.hub.docker.com/u/chronology/metis/), so you can do something like the following:

  * On a host machine, put a `settings.py` in `/etc/metis/settings.py`.  Note that the port in `settings.py` is ignored, as we communicate via nginx.
  * Run `docker run -v /etc/metis:/etc/metis -v /var/log/metis/:/var/log/metis/ -p PUBLIC_PORT:80 chronology/metis:v0.7.1`
  * Check `/var/log/metis` for app/nginx logs.

## How to build/push future versions

  * `./build.sh [git hash or tag you want to build] chronology/metis:v[version]`
  * `python ../../docker_tools/manage_docker.py push --tag chronology/metis:v[version]`
