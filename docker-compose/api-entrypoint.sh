#!/bin/bash

echo 'starting server'
poetry run gunicorn -w 2 --bind 0.0.0.0:5000 "api_gateway.app:create_app()"
