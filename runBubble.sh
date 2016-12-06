#!/bin/sh
python posTagger.py
cd bubble
python -m SimpleHTTPServer &
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --enable-speech-input 0.0.0.0:8000
