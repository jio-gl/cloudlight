#!/bin/bash

echo;echo mkdir $2;
mkdir $2;

types=(node link)
#lookaheads=(1 2 3)
lookaheads=(1)

echo;echo ./export_degree.py $1 $2degree.table;
time ./export_degree.py $1 $2degree.table;
echo;echo ./export_knn.py $1 $2knn.table;
time ./export_knn.py $1 $2knn.table;
echo;echo ./export_clustering.py $1 $2clustering.table;
time ./export_clustering.py $1 $2clustering.table;
echo;echo ./export_kcore.py $1 $2kcore.table;
time ./export_kcore.py $1 $2kcore.table;
echo;echo ./export_triangles.py $1 $2triangles.table;
time ./export_triangles.py $1 $2triangles.table;
for type in "${types[@]}"; do
	for lookahead in "${lookaheads[@]}"; do
		echo;echo ./export_degree.py $1 $2${type}sphere${lookahead}.table;
		time ./export_degree.py $1 $2${type}sphere${lookahead}.table;
	done
done

echo;echo sort -n $2degree.table > $2degree.txt.sorted;
sort -n $2degree.table > $2degree.txt.sorted;
echo;echo sort -n $2knn.table > $2knn.txt.sorted;
sort -n $2knn.table > $2knn.txt.sorted;
echo;echo sort -n $2clustering.table > $2clustering.txt.sorted;
sort -n $2clustering.table > $2clustering.txt.sorted;
echo;echo sort -n $2kcore.table > $2kcore.txt.sorted;
sort -n $2kcore.table > $2kcore.txt.sorted;
echo;echo sort -n $2triangles.table > $2triangles.txt.sorted;
sort -n $2triangles.table > $2triangles.txt.sorted;
for type in "${types[@]}"; do
	for lookahead in "${lookaheads[@]}"; do
		echo;echo sort -n $2${type}sphere${lookahead}.table > $2${type}sphere${lookahead}.txt.sorted;
		sort -n $2${type}sphere${lookahead}.table > $2${type}sphere${lookahead}.txt.sorted;		
	done
done

echo;echo cat $2degree.txt.sorted | cut -f 1 > $2nodes.txt;
cat $2degree.txt.sorted | cut -f 1 > $2nodes.txt;

echo;echo cat $2degree.txt.sorted | cut -f 3 > $2degree.txt
cat $2degree.txt.sorted | cut -f 3 > $2degree.txt
echo;echo cat $2knn.txt.sorted | cut -f 3 > $2knn.txt
cat $2knn.txt.sorted | cut -f 3 > $2knn.txt
echo;echo cat $2clustering.txt.sorted | cut -f 3 > $2clustering.txt
cat $2clustering.txt.sorted | cut -f 3 > $2clustering.txt
echo;echo cat $2kcore.txt.sorted | cut -f 3 > $2kcore.txt
cat $2kcore.txt.sorted | cut -f 3 > $2kcore.txt
echo;echo cat $2triangles.txt.sorted | cut -f 3 > $2triangles.txt
cat $2triangles.txt.sorted | cut -f 3 > $2triangles.txt
for type in "${types[@]}"; do
	for lookahead in "${lookaheads[@]}"; do
		echo;echo cat $2${type}sphere${lookahead}.txt.sorted | cut -f 3 > $2${type}sphere${lookahead}.txt
		cat $2${type}sphere${lookahead}.txt.sorted | cut -f 3 > $2${type}sphere${lookahead}.txt
	done
done

echo;echo ./complete_big_analysis.py $1 $2
time ./complete_big_analysis.py $1 $2
