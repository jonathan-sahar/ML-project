#!/bin/bash
branches=`cat $1`;
commit_id=$2;
cdcode;
echo  "picking: " $commit_id;
for branch in branches; do 
    Gcheckout $branch; 
    git cherry-pick --strategy=recursive -X theirs $commit_id; 
    Gpush_origin $1; 
done
