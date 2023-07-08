#! /bin/bash

set -x

ip netns del h1
ip netns del h2
ip netns del switch