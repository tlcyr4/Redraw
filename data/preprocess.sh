#!/bin/bash

# auxiliary python scripts
echo '
from __future__ import print_function
import sys

# python implementation of unix join (keep left)
# assumes sorted order

# usage: python join.py file1.tsv file2.tsv > joined
f1 = open(sys.argv[1])
f2 = open(sys.argv[2])

line2 = f2.readline()
tokens2 = line2.split("\t")

for line1 in f1:
    tokens1 = line1.strip("\n").split("\t")
    while tokens2[0] < tokens1[0]:
        line2 = f2.readline()
        if line2 == "":
            break
        tokens2 = line2.strip("\n").split("\t")
    while tokens2[0] == tokens1[0]:
        tokens1 += tokens2[1:]
        line2 = f2.readline()
        if line2 == "":
            break
        tokens2 = line2.strip("\n").split("\t")
    output = "\t".join(tokens1).replace("\n","")
    print(output)
' > join.py

echo '
#!/usr/bin/python

# replaces all instances of the aliases in a file with their standardized form
# read from stdin and write to stdout
from __future__ import print_function
import json
import sys
import re

# file where aliases are stored
aliases = json.load(open("aliases.json","r"))
regexes = {}
for line in sys.stdin:
    for entry in aliases:
        for alias in aliases[entry]:
            # cache compiled regexes for performance
            if alias not in regexes:
                regexes[alias] = re.compile(re.escape(alias), re.IGNORECASE)
            line = regexes[alias].sub(entry, line)
    sys.stdout.write(line)' > antialias.py


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
sed 's/0148 A/0592 /g' | 
sed 's/Africa/Forbes/g' | 
sed 's/\([A-Z]\)\([0-9][0-9][0-9]\)/\2/g' |
sed 's/Baseme/A /g' |
sed 's/\(0668 0[0-9][0-9] \)\(A\)/\10/g' |
sed 's/\(0094 [0-9]0[0-9] \)\(A\)/\10/g' |
sed 's/\(0023 [0-9][0-9] \)\(A\)/\10/g' |
sed 's/\(0023 T[0-9][0-9] \)\(A\)/\10/g' |
sed 's/\(0153 [78][12] \)\(1\)/\1A/g' |
sed 's/0023 62 2/0023 62 1/g' | #error by housing
sed 's/0153 73 2/0153 73 1/g' | #error by housing
sed 's/0153 74 2/0153 74 1/g' | #error by housing
sed 's/0153 75 3/0153 75 2/g' |
sed 's/0153 76 3/0153 76 2/g' |
sed 's/0153 77 4/0153 77 3/g' |
sed 's/0153 78 4/0153 78 3/g' |
sed 's/0153 83 2/0153 83 1/g' |
sed 's/0153 84 2/0153 84 1/g' |
sed 's/0153 85 3/0153 85 2/g' |
sed 's/0153 86 3/0153 86 2/g' |
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
    # join AVAIL18.tsv $f -t $'\t' >tmp # doesn't work
    python join.py AVAIL18.tsv $f >tmp
    mv tmp AVAIL18.tsv
    rm $f
done

tr -s "\t" <AVAIL18.tsv >tmp
mv tmp AVAIL18.tsv


echo '
import sys
import json
lists = json.load(sys.stdin)
dicts = {}
for room in lists:
    room[3] = str(room[3]).zfill(3)
    # if room[3][0] == "B":
    #     room[3] = "0" + room[3][1:]
    dicts[room[12] + " " + room[3]] = {
        "draw"  : room[0],
        "level"   : room[2],
        "sqft"  : room[4],
        "occ"   : room[5],
        "num_rooms":    room[6],
        "sub_free":     room[8]=="Y",
        "bathroom":     room[11]
    }
json.dump(dicts, sys.stdout, indent=4)
' > taclean.py

# preprocess tigerapp json
cat tigerapps.json |
sed 's/B\([0-9][0-9][0-9]\)/\1/g' |
python antialias.py |
sed 's/0148 College/Forbes/g' |
sed 's/ College//g' | python taclean.py |
sed 's/\([A-Z]\)\([0-9][0-9][0-9]\)/\2/g' > taclean.json

echo '
import json
import sys
taclean = json.load(open("taclean.json", "r"))
rooms = []
for line in sys.stdin:
    tokens = line.strip("\n").split("\t")
    if tokens[0].split()[0] == "0148":
        if tokens[0].split()[1] in "125 177 175 178":
            num_rooms = 2
        else:
            num_rooms = 1
    else:
        num_rooms = taclean[tokens[0]]["num_rooms"]
    if tokens[0].split()[0] in "0042 0007 0043 0047 0049 0091 0164" and tokens[4] == "A":
        tokens[4] = "0"
    if tokens[0].split()[0] in "0671":
        tokens[4] = str(int(tokens[4]) - 1)
    rooms.append({
        "building": tokens[0].split()[0],
        "number":   tokens[0].split()[1],
        "occ":    tokens[1],
        "draw":     tokens[2],
        "bathroom": tokens[3],
        "level":      tokens[4],
        "sqft":     tokens[5],
        "sub_free": tokens[6],
        "draw_rank":tokens[7::2],
        "size_rank":tokens[8::2],
        "num_rooms":num_rooms
    })
json.dump(rooms, sys.stdout, indent=4)
' > getnumrooms.py
cat AVAIL18.tsv | sort | python getnumrooms.py > AVAIL18.json

echo '
import json
import sys
from os import path
from glob import glob
out_polygons = {}
for polyfile in glob("polygons/*.json"):
    polygons = json.load(open(polyfile, "r"))
    building = path.basename(polyfile)[:4]
    # level = path.basename(polyfile)[-6]
    for polygon in polygons:
        level = polygon["level"]
        id = building + " " + level + " " + polygon["number"].zfill(3)
        x0 = polygon["origin"][0]
        y0 = polygon["origin"][1]
        if building == "0668" and level in ["0", "00"]:
            y0 -= 500
        # xrat = 10200.0 / float(polygon["dimensions"][1])
        # yrat = 6600.0 / float(polygon["dimensions"][0])
        xpad = (10200 - polygon["dimensions"][1])/2
        ypad = (6600 - polygon["dimensions"][0]) / 2
        points = [[point[0][0] + x0 + xpad, point[0][1] + y0 + ypad] for point in polygon["polygon"]]
        if id not in out_polygons:
            out_polygons[id] = []
        out_polygons[id].append(points)
print len(out_polygons)
json.dump(out_polygons, open("polygons.json", "w"), indent=4, sort_keys=True)
' > polygons.py
python polygons.py

echo '
import json

log = open("matching.log","w")
rf = open("AVAIL18.json","r")
rooms = json.load(rf)
polygons = json.load(open("polygons.json", "r"))
misses = 0
hits = 0
missfloor = {}
for room in rooms:
    id = room["building"] + " " + room["level"] + " " + room["number"]
    
    if id in polygons:
        hits += 1
        room["polygons"] = polygons[room["building"] + " " + room["level"] + " " + room["number"]]
        del polygons[room["building"] + " " + room["level"] + " " + room["number"]]
        polygons[room["building"] + " " + room["level"] + " " + room["number"] +"used"] = True
    else:
        log.write(room["building"] + " " + room["level"] + " " + room["number"] + "\n")
        room["polygons"] = []
        misses += 1
        if room["building"] + " " + room["level"] not in missfloor:
            missfloor[room["building"] + " " + room["level"]] = 0
        missfloor[room["building"] + " " + room["level"]] += 1
rf.close()
json.dump(rooms, open("AVAIL18.json", "w"), indent=4, sort_keys=True)
log.write("Hits: " + str(hits) + "\n")
log.write("Misses: " +  str(misses) + "\n")
missbldg = {}
for k,v in missfloor.items():
    bldg,level = map(str,k.split())
    if bldg not in missbldg:
        missbldg[bldg] = {}
    missbldg[bldg][level] = v
log.write("Misses by floor\n\n")
[log.write(str(bldg) + "\t" + str(missbldg[bldg]) + "\n") for bldg in missbldg]

log.write("used: " + str(len([polygon for polygon in polygons if "used" in polygon])) + "\n")
log.write("unused: " + str(len([polygon for polygon in polygons if "used" not in polygon])) + "\n")
unused = {}
for k,v in polygons.items():
    if "used" in k: continue
    bldg, level, num = map(str,k.split())
    # level = level[0]
    if bldg not in unused:
        unused[bldg] = {}
    if level not in unused[bldg]:
        unused[bldg][level] = 0
    unused[bldg][level] += 1
log.write("Unused by floor\n\n")
[log.write(bldg + "\t" + str(unused[bldg]) + "\n") for bldg in unused]
' > addpoly.py

# sed -i 's/\([TA]\)\([0-9][0-9]\)/\2/g' AVAIL18.json

python addpoly.py

echo '
import json
bf = open("buildings_clean.json", "r")
buildings = json.load(bf)
polygons = json.load(open("building_polygons.json", "r"))
for building in buildings.values():
    for polygon in polygons:
        if polygon["properties"]["id"] == building["id"]:
            building["polygons"] = polygon["geometry"]["coordinates"]
bf.close()
json.dump(buildings, open("buildings_clean.json", "w"), indent=4)
' > buildingpoly.py
cat buildings.json |
# sed 's/ Halls?//g' |
# sed 's/ College//g' |
# sed 's/Class of //g>' |
cat > buildings_clean.json
python buildingpoly.py

rm taclean.json polygons.json

rm join.py antialias.py getnumrooms.py polygons.py taclean.py buildingpoly.py addpoly.py