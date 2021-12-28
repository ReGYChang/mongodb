#!/bin/bash

for f in ./*.txt; do
    mv -- "$f" "${f%.txt}.js" 
done

python ./health_check_repl.py

python ./keyhole.py
