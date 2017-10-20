#!/bin/bash

FOLDER=tesis
TAKE=1

echo "nice -n 15 ./build_db_symmetric.py $1 $1.take$TAKE.big_graph $2 >> /$FOLDER/build_db_symmetric.log;"
nice -n 15 ./build_db_symmetric.py $1 $1.take$TAKE.big_graph $2 >> /$FOLDER/build_db_symmetric.log;

echo "nice -n 15 ./index_db_degree.py $1.take$TAKE.big_graph >> /$FOLDER/index_db_degree.log;"
nice -n 15 ./index_db_degree.py $1.take$TAKE.big_graph >> /$FOLDER/index_db_degree.log;

echo "nice -n 15 ./drop_index_db_unseen_degree.py $1.take$TAKE.big_graph >> /$FOLDER/drop_index_db_unseen_degree.log;"
nice -n 15 ./drop_index_db_unseen_degree.py $1.take$TAKE.big_graph >> /$FOLDER/drop_index_db_unseen_degree.log;

echo "nice -n 15 ./index_db_unseen_degree.py $1.take$TAKE.big_graph >> /$FOLDER/index_db_unseen_degree.log;"
nice -n 15 ./index_db_unseen_degree.py $1.take$TAKE.big_graph >> /$FOLDER/index_db_unseen_degree.log;

#echo "nice -n 15 ./test_privacy_passive.py $1.take$TAKE.big_graph $1.take$TAKE.big_graph.passive > /$FOLDER/test_privacy_passive-lj-take$TAKE.log;"
#nice -n 15 ./test_privacy_passive.py $1.take$TAKE.big_graph $1.take$TAKE.big_graph.passive > /$FOLDER/test_privacy_passive-lj-take$TAKE.log
