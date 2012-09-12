#!/bin/bash

SETTINGS=$1
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
./graph.py $DIR/weather.conf
