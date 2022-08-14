#!/bin/bash
set -e
. /root/.bashrc
python3 seg.py "$@"
