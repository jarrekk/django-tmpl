#!/usr/bin/env bash
# author: Kun Jia
# date: 9/1/17
# email: me@jarrekk.com
set -e
cmd="$@"

echo entrypoint

exec ${cmd}
