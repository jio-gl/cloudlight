#!/bin/bash

# $1 archivo fuente con links
# $2 carpeta
# $3 archivo sin extension
# $4 cantidad de links
# $5 attack set
# $6 coverage types (comma separated)
# $7 end converage 50, 60, 95, etc
# $8 "index" or something not-null to index from scratch


if [ -n "$8" ]
    then

    echo
    echo "rm $2$3.*;"
    rm $2$3.*;
    echo
    echo "./build_db.py $1 $2$3.big_graph $4 > $2$3.log;";
    ./build_db.py $1 $2$3.big_graph $4  > $2$3.log;
    echo
    echo "./index_db_degree.py $2$3.big_graph >> $2$3.log ;"
    ./index_db_degree.py $2$3.big_graph >> $2$3.log ;
    echo
    echo "./index_db_triangles.py $2$3.big_graph >> $2$3.log;"
    ./index_db_triangles.py $2$3.big_graph >> $2$3.log; 
    echo
    echo "./index_db_unseen_triangles.py $2$3.big_graph >> $2$3.log ;"
    ./index_db_unseen_triangles.py $2$3.big_graph >> $2$3.log ;
    echo
    echo "./index_db_unseen_degree.py $2$3.big_graph >> $2$3.log ;"
    ./index_db_unseen_degree.py $2$3.big_graph >> $2$3.log ;
    echo
    echo "./index_db_seen_degree.py $2$3.big_graph >> $2$3.log ;"
    ./index_db_seen_degree.py $2$3.big_graph >> $2$3.log ;
    echo
    echo "./index_db_seen_triangles.py $2$3.big_graph >> $2$3.log ;"
    ./index_db_seen_triangles.py $2$3.big_graph >> $2$3.log ;

fi
echo
echo "./test_big_privacy.py $2$3.big_graph $2$3.$5.$6 $5 $6 $7 >> $2$3.log ;"
./test_big_privacy.py $2$3.big_graph $2$3.$5.$6 $5 $6 $7 >> $2$3.log ;
