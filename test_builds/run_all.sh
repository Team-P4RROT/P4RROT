
for dirname in $(ls | grep '\.test')
do
    echo "##### $dirname"
    cd $dirname
    bash test.sh
    cd ..
done