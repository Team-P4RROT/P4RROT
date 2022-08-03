This case tests the BloomFilter implementation defined in stateful.py.
`codegen.py` defines a BloomFilter with a register of length 1000, using 3 hash functions. Feel free to change these values.

The `client.py` file is a manual client, you can use it to manually put or check values.
The automated_client.py script executes 500 puts and 1000 gets, and calculates the false positive rate of the implementation.
This can be used to experiment with different sizes and a different number of hash functions.

To run this test case:
```
./test.sh
sudo p4app run test.p4app

mininet> h1 exec python3 /tmp/automated_client.py 10.0.0.1
```