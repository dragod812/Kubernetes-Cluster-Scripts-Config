#!/bin/bash
nohup bash ../scripts/start.sh > nifi-out.log 2>&1 &
exec python3.6 $@
