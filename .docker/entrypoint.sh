#!/usr/bin/env bash

cd /opt/omni/technical-test

# image can run in multiple modes
if [[ "${1}" == "shell" ]]; then
    exec /bin/bash
elif [[ "${1}" == "migrate-noinput" ]]; then
    exec python manage.py migrate --noinput
elif [[ "${1}" == "collectstatic" ]]; then
    exec python manage.py collectstatic --noinput
elif [[ "${1}" == "celery" ]]; then
    APP="${APP:-tecnical_test}"
    QUEUES="${QUEUES:-celery}"
    LOG_LEVEL="${LOG_LEVEL:-info}"
    CONCURRENCY="${CONCURRENCY:-1}"
    MAX_TASKS="${MAX_TASKS:-1000}"

    exec celery -A $APP -l $LOG_LEVEL -c $CONCURRENCY --maxtasksperchild=$MAX_TASKS worker -Q $QUEUES

else

    exec gunicorn --config=gunicorn_config.py technical_test.wsgi

fi