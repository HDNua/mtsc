i=0
while [ "$i" -lt 10000 ]
do
    i=$(expr $i + 1)
    echo $i

    ./run.sh
done
