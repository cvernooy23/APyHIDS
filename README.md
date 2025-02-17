# APyHIDS

## Introduction

## Intention

this is just a small personal project to write a HIDS in python3, because why not? Eventually I will probably turn it into a binary and have the agents write to a database. if I have time


### Required Libraries 

I used venv, you can do whatever.

- yaml
- certifi
- charset
- idna
- psutil
- pyyaml
- requests
- urllib3
- watchdog
- pip

python3 built in modules used:
- time
- multiprocessing
- os
- queue
- pathlib

### Run

if using venv  
`source <where you cloned this>/app/bin/activate`


`python3 main.py`

> [!WARNING]  
> Don't run this on a single core machine, unless you want it to become unresponsive. Tested on a VM (AL 2023) in my homelab with 4 cores and 2048MB of memory