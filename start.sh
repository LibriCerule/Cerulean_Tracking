#!/bin/bash

if [ $# != 1 ]; then
  echo "Usage: start.sh [IP address]"
  exit 1
fi

python web.py $1
