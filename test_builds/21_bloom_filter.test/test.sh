
function compare_code
{
    diff -E -Z -b -w -B $1 ../$1 
}

sudo rm -r test.p4app
cp -r ../../p4_template.p4app test.p4app
python3 codegen.py

cp client.py test.p4app/
cp automated_client.py test.p4app/

cd test.p4app
echo '*' > .gitignore
bash build.sh > buildlog.txt

cat buildlog.txt | grep "BMV2 BUILD SUCCEDED"
cat buildlog.txt | grep "NFP BUILD SUCCEDED"
compare_code a_headers.p4
compare_code a_hdrlist.p4
compare_code a_chains.p4
compare_code a_declarations.p4
compare_code a_apply.p4

