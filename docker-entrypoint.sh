#!/usr/bin/env bash

# Always use Bash for this entrypoint. sh (Dash) removes
# variables with dots in the name from the environment.

set -euo pipefail

for p in /run/exabgp/exabgp.in /run/exabgp/exabgp.out; do
    if ! [ -e "$p" ]; then
        mkfifo "$p"
    fi
    chmod 0600 "$p"
done

exec "$@"
