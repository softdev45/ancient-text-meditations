#!/bin/bash
(flask --app main run) & ( cd words && python word_service.py ) &
