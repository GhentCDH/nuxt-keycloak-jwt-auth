#!/bin/sh

# Persistent data storage for docker container data 

# store keycloak data base data base data
mkdir -p ./docker/data/keycloak_db

# Not strictly needed but practical during dev:
# store home directories for history and persistent config.
mkdir -p ./docker/data/frontend_homedir
mkdir -p ./docker/data/backend_homedir
