#!/bin/bash

datadog-agent run > /dev/null &
/opt/datadog-agent/embedded/bin/trace-agent --config=/etc/datadog-agent/datadog.yaml > /dev/null &
/opt/datadog-agent/embedded/bin/process-agent --config=/etc/datadog-agent/datadog.yaml > /dev/null &
ddtrace-run poetry run gunicorn -w 4 --log-level=debug --bind 0.0.0.0:$PORT "api_gateway.app:create_app()"
