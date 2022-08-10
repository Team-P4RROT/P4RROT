
for dirname in $(ls | grep '\.test')
do
    echo "##### $dirname"
    cd $dirname
    for fname in $(ls tmp.p4app | grep -e '^a_')
    do
        cp tmp.p4app/$fname test.p4app/$fname
    done
    cd ..
done
