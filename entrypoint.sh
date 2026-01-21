#!/bin/bash

# Wait for MariaDB to be ready
echo "Waiting for MariaDB..."
while ! nc -z db 3306; do
  sleep 0.1
done
echo "MariaDB is ready!"

# Initialize database
flask init-db

# Start the application
exec "$@"
