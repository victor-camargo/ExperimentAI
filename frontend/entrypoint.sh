#!/bin/sh
# Copy pre-built files to the volume
cp -a /app/dist/. /app/volume/
# Keep the container running (or replace with your own command, e.g., `npm start`)
tail -f /dev/null