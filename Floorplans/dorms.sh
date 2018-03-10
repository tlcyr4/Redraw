while read line; do
    set -- $line
    if [ ! -d $2 ]; then
        mkdir $2
        mv $1*.png $2
    fi
done