#!/bin/sh
gunicorn --chdir app manage:app -w 4 -b :8080