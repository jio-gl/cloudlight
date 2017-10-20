#!/bin/bash

echo "time ./build_db.py $1 $1-$2.big_graph $2 >> $1-$2.big_graph.log;"
time ./build_db.py $1 $1-$2.big_graph $2 >> $1-$2.big_graph.log;

echo "time ./index_db_all.py $1-$2.big_graph >> $1-$2.big_graph.log;"
time ./index_db_all.py $1-$2.big_graph >> $1-$2.big_graph.log;

echo "time ./complete_big_analysis.sh $1-$2.big_graph $1-$2.big_graph.analysis/ >> $1-$2.big_graph.log;"
time ./complete_big_analysis.sh $1-$2.big_graph $1-$2.big_graph.analysis/ >> $1-$2.big_graph.log;
