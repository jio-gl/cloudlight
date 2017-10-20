#!/bin/bash

cat $1  | awk -F'[ ]' '{ if ( <= ) print , ; else print ,  }' | sort | uniq -d > $1.symm
