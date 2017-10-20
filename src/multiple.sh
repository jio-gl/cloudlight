#!/bin/bash

RUNS=20

./privacy_run.sh $1 $2 $3 $4 $5 $6 $7 $8;

let RUNS=$RUNS-1
for i in `seq 0 $RUNS`;
do
	cp $2$3.big_graph $2$3-$i.big_graph;
	./privacy_run.sh $1 $2 $3-$i $4 $5 $6 $7;
done

let RUNS=$RUNS+1
./postprocess-runs.py $2 $3 $5 $6 $RUNS;
