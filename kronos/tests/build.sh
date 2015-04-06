#!/bin/sh

python ../../docker_tools/manage_docker.py export --hash $1 --export-path $(git rev-parse --show-toplevel)/kronos/tests/chronology --repository-path $(git rev-parse --show-toplevel) && \
python ../../docker_tools/manage_docker.py build --dockerfile-directory . --tag $2
