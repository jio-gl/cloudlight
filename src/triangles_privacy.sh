#!/bin/bash

date >> /large/jorlicki/lj-10mill.log;
./build_db_symmetric.py /large/jorlicki/livejournal-links.txt /large/jorlicki/lj-10mill.big_graph 10000000 >> /large/jorlicki/lj-10mill.log;

date >> /large/jorlicki/lj-10mill.log;
./index_db_degree.py /large/jorlicki/lj-10mill.big_graph >> /large/jorlicki/lj-10mill.log;

date >> /large/jorlicki/lj-10mill.log;
./index_db_triangles.py /large/jorlicki/lj-10mill.big_graph >> /large/jorlicki/lj-10mill.log; 

date >> /large/jorlicki/lj-10mill.log;
./index_db_unseen_triangles.py /large/jorlicki/lj-10mill.big_graph >> /large/jorlicki/lj-10mill.log;

date >> /large/jorlicki/lj-10mill.log;
./index_db_seen_triangles.py /large/jorlicki/lj-10mill.big_graph >> /large/jorlicki/lj-10mill.log;

date >> /large/jorlicki/lj-10mill.log;
./test_big_privacy.py /large/jorlicki/lj-10mill.big_graph /large/jorlicki/lj-10mill.triangles.triangle triangles triangle >> /large/jorlicki/lj-10mill.log;


