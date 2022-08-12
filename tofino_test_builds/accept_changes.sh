
for dirname in $(ls | grep '\.test')
do
    echo "##### $dirname"
    cd $dirname
    for fname in $(ls result.p4app | grep -e '^a_')
    do
        echo "    $fname"
        cp result.p4app/$fname test.p4app/$fname
    done
    cd ..
done
