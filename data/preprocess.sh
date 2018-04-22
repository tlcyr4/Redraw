#!/bin/bash

# available rooms

sed 's/\r//g' AVAIL18.txt |
sed 's/SINGLE/\n1/g'  |
sed 's/DOUBLE/\n2/g' |
sed 's/TRIPLE/\n3/g' |
sed 's/QUAD/\n4/g' |
sed 's/QUINT/\n5/g' |
sed 's/6PERSON/\n6/g' |
sed 's/7PERSON/\n7/g' |
sed 's/8PERSON/\n8/g' |
sed 's/9PERSON/\n9/g' |
sed 's/10PERSON/\n10/g' |
awk '/[0-9]/{print $0}' |
sed 's/\ College//g' |
#shield forbes
sed 's/Forbes/Africa/g' |
python antialias.py |
sed 's/Africa/Forbes/g' |
sed 's/\([A-Z]\)\([0-9][0-9][0-9]\)/\2/g' |
sed 's/\(B\)\([0-9][0-9]\)/A\2/g' |
sed 's/Baseme/A /g' |
awk '{if($4=="bathroom") $4=""; else $3 = "Pub\t"$3; print $0}' |
sed 's/Private/Prv/g' | sed 's/Shared/Sha/g' |
awk '{if($8!="Yes") $8="No "$8;print $0}' |
awk '{if($9=="Independent") $2="Independent";if($4=="0153")$2="Spelman";$9="";print $0}' |
awk '{if(length($5)<3) $5=sprintf("%03d",$5); print $0}' |
awk '{print $4" "$5 >"tmp1"; $4=$5=""; print $0}' | tr " " "\t" >tmp2



paste -d "\t" tmp1 tmp2 |
tr -s " " | sort >AVAIL18.tsv
rm tmp1 tmp2

# past draws
for f in $(ls HRD*.txt); do
    sed 's/\r//g' $f |
    python antialias.py > $f.new
    sed -i '/^$/d' $f.new;
done

awk '/[0-9]/{print $7"\t"$6}' HRD11.txt.new > HRD11.tsv
awk '/[0-9]/{print $2"\t"$1}' HRD14.txt.new | python antialias.py > HRD14.tsv
awk '/[0-9]/{print $1"\t"$2}' HRD16.txt.new > HRD16.tsv
awk '/[0-9]/{print $1"\t"$2}' HRD17.txt.new > HRD17.tsv
rm *.new
# rm HRD17.tsv
for f in $(ls HRD*.tsv); do
    echo $f
    awk '!x[$1"\t"$2]++' $f |
    sed 's/WENDELL\tC/0670\t/g' |
    sed 's/WENDELL\tB/0669\t/g' |
    sed 's/BAKER\tE/0673\t/g' |
    sed 's/BAKER\tS/0686\t/g' |
    sed 's/FORBES\tA/0148\t/g' |

    sed 's/\([A-Z]\)\([0-9][0-9][0-9]\)/\2/g' |
    tr "\t" " " |

    awk '{printf($0"\t%04d\n",NR)}' |
    sort >tmp
    mv tmp $f
    # add draws
    join $f AVAIL18.tsv -t $'\t' -o 1.2,1.1,2.2,2.3 | sort |
    awk '{print $2"\t"$3"\t"$4"\t"$5}' |
    awk '{
        key=$4;
        if(!(key in drawranks))drawranks[key]=0;
        drawranks[key]+=1;
        $5=drawranks[key];
        key=$3$4;
        if(!(key in sizeranks))sizeranks[key]=0;
        sizeranks[key]+=1;
        $6=sizeranks[key];
        print $0
        }' |
    awk '{print $1" "$2"\t"$5"\t"$6}' |
    sort >$f
    
done

for f in $(ls HRD*.tsv); do
    # join AVAIL18.tsv $f -t $'\t' >tmp
    python join.py AVAIL18.tsv $f >tmp
    mv tmp AVAIL18.tsv
done

tr -s "\t" <AVAIL18.tsv >tmp
mv tmp AVAIL18.tsv
# sed -i 's/\t\t\t/\t/g' AVAIL18.tsv
