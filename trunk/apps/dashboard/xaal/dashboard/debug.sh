#!/bin/sh

while true; do
  python app.py &
  PID=$!
  hl "App started.."
  sleep 1
  inotifywait -r . -e modify -e create -e delete --exclude '(\.mako|\.tag)'
  hl "Killing app"
  kill $PID
done
