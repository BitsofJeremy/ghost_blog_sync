#!/usr/bin/env bash

# local directory is SCRIPT_DIR
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate the virtualenv
source "$SCRIPT_DIR/venv/bin/activate"

# Run the app
"$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/blog_sync.py"
