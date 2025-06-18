#!/bin/bash
source venv/bin/activate
exec gunicorn -k uvicorn.workers.UvicornWorker fastapp:app --bind 0.0.0.0:8000
