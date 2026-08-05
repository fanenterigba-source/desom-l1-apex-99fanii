#!/bin/bash
python desom_l1_ws.py &
python -m http.server $PORT &
wait
