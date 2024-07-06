#!/bin/bash

export PYTHONPATH=/app

flask run --host=0.0.0.0 &

sleep 20

python3 /app/src/kafka/consumer.py
