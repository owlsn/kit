#!/usr/bin/bash
`ps -ef | grep -v grep | grep sched.py | awk -F ' ' '{print $2}' | xargs kill -9`
`cd /home/ubuntu/workspace/kit/spiders/ip_proxy/ip_proxy && /home/ubuntu/workspace/kit/venv/bin/python3 sched.py`