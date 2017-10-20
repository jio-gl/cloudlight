#!/bin/bash

FOLDER=large
TAKE=6

./build_db_symmetric.py /$FOLDER/jorlicki/livejournal-links.txt /$FOLDER/jorlicki/livejournal-links.txt.sym-40mill-take$TAKE.big_graph 40000000 >> /$FOLDER/jorlicki/livejournal-links.txt.sym-40mill-take$TAKE.log;
./index_db_degree.py /$FOLDER/jorlicki/livejournal-links.txt.sym-40mill-take$TAKE.big_graph >> /$FOLDER/jorlicki/livejournal-links.txt.sym-40mill-take$TAKE.log;
./drop_index_db_unseen_degree.py /$FOLDER/jorlicki/livejournal-links.txt.sym-40mill-take$TAKE.big_graph >> /$FOLDER/jorlicki/livejournal-links.txt.sym-40mill-take$TAKE.log;
./index_db_unseen_degree.py /$FOLDER/jorlicki/livejournal-links.txt.sym-40mill-take$TAKE.big_graph >> /$FOLDER/jorlicki/livejournal-links.txt.sym-40mill-take$TAKE.log;
./test_privacy_passive.py /$FOLDER/jorlicki/livejournal-links.txt.sym-40mill-take$TAKE.big_graph /$FOLDER/jorlicki/livejournal-links.txt.sym-40mill-take$TAKE.big_graph.passive >> /$FOLDER/jorlicki/livejournal-links.txt.sym-40mill-take$TAKE.log
