#!/bin/bash
gunicorn main:app --bind 0.0.0.0:5000 & gunicorn --chdir words word_service:app --bind 0.0.0.0:5001
