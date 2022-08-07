#!/bin/bash

for i in $(seq 1 5); do
   echo "{'server_name':'exec', 'repo_number': ${i}}"
   sleep 1
done
