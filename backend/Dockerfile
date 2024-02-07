########
# Base #
########
FROM python:3.12-slim-bookworm as python-base

# gcc is required to install Litestar (multidict dependency)
# cargo is required to install Litestar (multidict dependency)
RUN apt-get update && apt-get install -y gcc cargo

# Install PDM
RUN pip install -U pip setuptools wheel && pip install pdm


##############
# Target dev #
##############
FROM python-base as dev

# Some additional development tools which can be practical during debugging / development
RUN apt-get update && apt-get install -y micro ncdu htop fzf ripgrep git telnet iputils-ping git

WORKDIR /app
