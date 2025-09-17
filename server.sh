#!/bin/bash

if [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

if [ "$1" == "dev" ]; then
    fastapi dev server.py
else
    echo "run with './server.sh dev' for development mode"
    fastapi run server.py
fi

