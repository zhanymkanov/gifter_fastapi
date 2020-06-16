#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app --exclude=__init__.py
isort --recursive --apply app
black app
