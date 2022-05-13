This case tests the Stack implementation defined in stateful.py.
The `client.py` is a simple test client that can push 2 values to the stack then pops them (the order should be reversed)

To run this test case:
```
./test.sh
sudo p4app run test.p4app

mininet> h1 exec python3 /tmp/client.py 10.0.0.1
```