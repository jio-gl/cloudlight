#!/bin/bash

FOLDER=experiments
TAKE=5

nice -n 15 ./build_db_symmetric.py /$FOLDER/jorlicki/livejournal-links.txt /$FOLDER/jorlicki/livejournal-links.txt.sym-take$TAKE.big_graph 100000000 >> /$FOLDER/jorlicki/build_db_symmetric.log;
nice -n 15 ./index_db_degree.py /$FOLDER/jorlicki/livejournal-links.txt.sym-take$TAKE.big_graph >> /$FOLDER/jorlicki/index_db_degree.log;
nice -n 15 ./drop_index_db_unseen_degree.py /$FOLDER/jorlicki/livejournal-links.txt.sym-take$TAKE.big_graph >> /$FOLDER/jorlicki/drop_index_db_unseen_degree.log;
nice -n 15 ./index_db_unseen_degree.py /$FOLDER/jorlicki/livejournal-links.txt.sym-take$TAKE.big_graph >> /$FOLDER/jorlicki/index_db_unseen_degree.log;
nice -n 15 ./test_privacy_passive.py /$FOLDER/jorlicki/livejournal-links.txt.sym-take$TAKE.big_graph /$FOLDER/jorlicki/livejournal-links.txt.sym-take$TAKE.big_graph.passive > /$FOLDER/jorlicki/test_privacy_passive-lj-take$TAKE.log
