Running Tests
-------------
Unit tests for Kronos can be run by building and running a test docker image
with all the storage dependencies installed.

.. code:: sh
    ./build.sh {GIT_HASH} {DOCKER_IMAGE_NAME}
    docker run {DOCKER_IMAGE_NAME}

The test results will be printed to stdout.
