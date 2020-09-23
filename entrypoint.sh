#!/bin/bash

set -e

exec python pipeline_runner.py &
exec python main.py