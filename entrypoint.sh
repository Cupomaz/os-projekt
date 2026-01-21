#!/bin/bash

# Extract host and port from DATABASE_URL
# Format: mariadb+mysqldb://user:pass@host:port/database
DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')

# Default to db:3306 if extraction fails (for docker-compose)
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-3306}

# Wait for MariaDB to be ready
echo "Waiting for MariaDB at $DB_HOST:$DB_PORT..."
until nc -z $DB_HOST $DB_PORT; do
  echo "MariaDB is unavailable - sleeping"
  sleep 1
done
echo "MariaDB is ready!"

# Initialize database
flask init-db

# Start the application
exec "$@"
