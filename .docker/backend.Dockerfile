FROM python:3.8.3-slim-buster

# for access to private PyPI registry during build
# keys will not be visible in the final image history due to the multistage build

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # compiler for Python C modules
    g++ make libc6-dev

RUN groupadd -g 1337 omni && \
    useradd -m -d /opt/omni -u 1337 -g omni omni

USER omni

# install Python requirements
ADD requirements.txt /tmp/requirements.txt
ADD --chown=omni:omni .docker/dev /usr/bin

RUN dev pipi -r /tmp/requirements.txt && \
    # clean up Python modules
    find /opt/omni/.local \
    \( -type d -a -name test -o -name tests \) \
    -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
    -exec rm -rf '{}' \;

###

FROM python:3.8.3-slim-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    procps vim less

RUN groupadd -g 1337 omni && \
    useradd -m -d /opt/omni -u 1337 -g omni omni

USER omni
WORKDIR /opt/omni
ENV PATH /opt/omni/.local/bin:$PATH
COPY --chown=omni:omni --from=0 /opt/omni/.local /opt/omni/.local

EXPOSE 8000

ADD --chown=omni:omni .docker/entrypoint.sh /
ADD --chown=omni:omni .docker/dev /usr/local/bin

ENTRYPOINT ["/entrypoint.sh"]