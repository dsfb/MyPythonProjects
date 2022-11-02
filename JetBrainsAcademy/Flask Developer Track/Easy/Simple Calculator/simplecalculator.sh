#!/usr/bin/env bash

set -f
echo "Welcome to the basic calculator!" | tee operation_history.txt
re='^-?[0-9]+\.?[0-9]* [-,+,*,/,^] -?[0-9]+\.?[0-9]*$'

while true
do
  echo "Enter an arithmetic operation or type 'quit' to quit:" | tee -a operation_history.txt
  read operation
  echo $operation >> operation_history.txt
  if [[ "$operation" == "quit" ]]; then
    echo "Goodbye!" | tee -a operation_history.txt
    break
  elif [[ "$operation" =~ $re ]]; then
    bc -l <<< "scale=2; $operation" | tee -a operation_history.txt
  else
    echo "Operation check failed!" | tee -a operation_history.txt
  fi
done
