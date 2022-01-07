
for dirname in $(ls | grep '\.test')
do
    echo "##### $dirname"
    cd $dirname
    for fname in $(echo "a_apply.p4 a_chains.p4 a_declarations.p4 a_hdrlist.p4 a_headers.p4")
    do
        cp test.p4app/$fname ./$fname
    done
    cd ..
done
