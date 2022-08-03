# Balazs Notes
These are some of the questions I've had and the progress I've made when starting out with P4RROT development.
Hopefully someone finds it useful.

Got it up and running (Virtualbox+Docker), tested a few, e.g. barchoba. Trying to understand the code. Started to write a stateful stack based on the SharedArray.

* Is this a good starting exercise?
* What is the env? Is it the same as the test_env?
* Where should my temp index variable be declared? Is it correct to use a register<1> for storing the index long-term? Should that exist in the env, or can it be "internal"
* How to test what code it generates? What's a good dev workflow?



# 4/20
* Added a properties field to SharedElements. This can be used if we need to reuse some property of the SharedElement in related commands (e.g. with the bloom filter, we define its size and number of hash functions at declaration, but use this info in the commands)
* Implemented writes and reads