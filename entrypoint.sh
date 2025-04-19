#!/bin/sh

echo "Starting smartd_exporter loop..."

trap "echo 'Stopping smartd_exporter...'; exit 0" TERM INT

while true; do
  echo "[`date`] Running smartd_exporter.py"
  python /app/smartd_exporter.py
  sleep 300 &
  wait $!
done