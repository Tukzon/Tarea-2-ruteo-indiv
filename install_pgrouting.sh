#!/bin/bash
set -e

# Cambia al usuario root para instalar pgRouting
if [ "$(id -u)" = '0' ]; then
    apt-get update
    apt-get install -y --no-install-recommends postgresql-13-pgrouting
    apt-get clean
    rm -rf /var/lib/apt/lists/*
else
    # Si no es root, intenta cambiar al usuario root
    exec gosu root "$BASH_SOURCE" "$@"
fi
