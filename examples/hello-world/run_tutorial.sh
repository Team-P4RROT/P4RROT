
set -e

#
# remove previous attempts
#

if test -d "test.p4app"
then
    sudo rm -r test.p4app
fi

if test -d "p4app"
then
    rm -r -f p4app
fi

#
# get p4app
#

git clone https://github.com/p4lang/p4app

#
# get a template for BMv2
#

cp -r ../../templates/p4_template.p4app test.p4app

#
# run the code generator
#

python3 codegen.py

#
# build
#

sudo p4app/p4app build test.p4app


#
# run
#

x-terminal-emulator -e sudo p4app/p4app run test.p4app &

echo '########################################'
echo '# PRESS ENTER WHEN MININET IS READY    #'
echo '########################################'
read

sudo p4app/p4app exec apt install -y netcat

echo '########################################'
echo '# PRESS ENTER WHEN READY TO RUN NETCAT #'
echo '########################################'
read

sudo p4app/p4app exec m h1 ifconfig h1-eth0 10.0.0.1/24
sudo p4app/p4app exec m h2 ifconfig h2-eth0 10.0.0.2/24

x-terminal-emulator -e "echo '[h1] NC client' ; sudo p4app/p4app exec m h1 nc -u 10.0.0.2 5555 ; read" &
x-terminal-emulator -e "echo '[h2] NC server' ; sudo p4app/p4app exec m h2 nc -ul -k -v -p 5555 ; read"

echo 'press enter to end...'
read