# P4RROT

Generating P4 Code for the Application Layer

## Motivation

Throughput and latency-critical applications (e.g. processing sensor data, robot control, or monitoring stock market streams) can often benefit if computations are performed close to the client. Performing these computations in the data plane can help us take it to the next level.

P4 is excellent data plane programming language, and we all love it. However, it wasn't meant to implement application-layer tasks. Thus, offloading server-functionality can be challenging.

P4RROT is a code generator that helps programmers overcome certain limitations and write shorter and easier-to-read code.

## Supported targets

P4RROT is a very young project. The current code base supports both the BMv2 and the Netronome NFP.

We plan to add Tofino specific elements as well.

## Getting started

...