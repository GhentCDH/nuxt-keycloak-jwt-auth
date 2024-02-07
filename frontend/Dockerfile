########
# Base #
########
FROM node:20-bookworm-slim as node-base

# Install pnpm globally
RUN npm install -g pnpm


##############
# Target dev #
##############
FROM node-base as dev

# Some additional development tools which can be practical during debugging / development
RUN apt-get update && apt-get install -y micro ncdu htop fzf ripgrep git telnet iputils-ping git telnet

WORKDIR /app

# For development:
# * code will be synced using a mounted volume configured using Docker compose
# * npm install --include=dev will be run using Docker compose command,
#   otherwise, there can be an inconsistency between a cached container and the installed packages
# * app is run as root user, because docker compose mounts named volumes as root exclusively on linux
#   (https://github.com/docker/compose/issues/3270)
