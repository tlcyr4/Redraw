# draws.sh
while read line; do
    set -- $line
    draw=$1
    read line
    set -- $line
    if [ ! -d $draw]; then 
        mkdir $draw 
    fi
    for dorm in $line; do
        if [$dorm]; then
            mv $dorm $draw
        else
            cp Mathey/$dorm
        done
    done
done
cp Mathey/Campbell 