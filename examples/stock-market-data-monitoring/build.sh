function compare_code
{
    diff -E -Z -b -w -B $1 ../$1 
}

sudo rm -r test.p4app
cp -r ../../templates/p4_template.p4app test.p4app

python3 codegen.py

cd test.p4app
echo '*' > .gitignore
bash build.sh > buildlog.txt

cat buildlog.txt | grep "BMV2 BUILD SUCCEDED"
cat buildlog.txt | grep "NFP BUILD SUCCEDED"