#!/bin/bash
cd backend-flask
python -m flask run --host=0.0.0.0 --port=$PORT
