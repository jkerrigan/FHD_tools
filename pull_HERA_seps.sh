#! /bin/bash


bls=$(python ./find_seps.py ~/data/jkerriga/HERAPSPEC/even/zen.2458042.20009.xx.HH.uvOR)
split=(even odd)
base_dir=~/data/jkerriga/HERAPSPEC/
echo $bls
for i in "${split[@]}";do
    echo $i
    cd ${base_dir}${i}
    python ~/capo/dcj/scripts/pull_antpols.py -a $bls ./*uvOR
done