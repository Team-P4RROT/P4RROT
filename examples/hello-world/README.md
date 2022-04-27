# A Hello World Tutorial

What else would be the best first task for P4RROT than teaching it to say HELLO? :)

In this tutorial, you can try out P4RROT using the BMv2 target on a Linux system.

What you need to have before starting: Python3, Docker, git, terminal emulator.

## 1. Get P4RROT

First of all, we get a copy of P4RROT and this tutorial.

```console
git clone https://github.com/gycsaba96/P4RROT
```

Now, let's switch to this example's directory.

```console
cd P4RROT/examples/hello-world
```

The following steps are also available in a single bash script (run_tutorial.sh) for your convenience.

## 2. Get p4app

We will use p4app as a convenient prepackaged way to build and run P4 code.

```console
git clone https://github.com/p4lang/p4app
```

## 3. Get a template for BMv2

First, we chose a P4 template that suits our goals. Since we write code for the BMv2 target we use the one in P4RROT/templates/p4_template.p4app. It is already prepared for use in p4app. (This template would also work for the Netronome smartNIC.)

Just copy the template to our working directory:

```console
cp -r ../../templates/p4_template.p4app test.p4app
```

## 4. Write a Python code using P4RROT

Let's write our code in a file called `codegen.py`.

### a) Import P4RROT modules

To save you from creating a venv and installing P4RROT we choose the less elegant way by inserting the source directory into the Python-path.

After that we import certain modules:
- `p4rrot.generator_tools` : classes and helper functios to support general code generation,
- `p4rrot.known_types` : supported types in P4RROT,
- `p4rrot.standard_fields` : often used header fields,
- `p4rrot.core.commands` : these commands depend only on the P4 specification.


```python
import sys
sys.path.append('../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.standard_fields import *
from p4rrot.core.commands import * 
```

> **_NOTE:_**  BMv2 uses the v1model architecture. We could also import commands and stateful elements specific to v1 model from `p4rrot.v1model.commands` and `p4rrot.v1model.stateful`. Similarly, one can access tools meant for Intel Tofino.


### b) Create a FlowProcessor instance

We create a `FlowProcessor` instance, that will describe our processing. One may look at the instantiation as a specification/declaration for the processing. (Just like we inputs/outputs and local variables on many languages.)

We use 3 different 12 bytes long strings (one for input, one for output, and one as a temporal local variable) and a boolean value.

```python
fp = FlowProcessor(
        istruct = [('msg_in',string_t(12))],
        locals  = [('l',bool_t),('msg_tmp',string_t(12))],
        ostruct = [('msg_out',string_t(12))]
    )
```

> **_NOTE:_**  If we do not define `ostruct`, the modified `istruct` are kept.

### c) Describe the processing steps using Commands

Now that we have a flow processor object, we can populate it with `Commands`. These are basically the statements of our algorithm. 

If the `msg_in` has the value 'Hello World!', we send back the packet with a new message. Otherwise, we just copy the input to the output. 

Thanks to method chaining and a proper indentation, we can create a fairly readable code.


```python
(
fp
.add(AssignConst('msg_tmp',b'Hello World!'))
.add(Equals('l','msg_in','msg_tmp'))
.add(If('l'))
          .add(AssignConst('msg_out',b'HELLO! :)   '))
          .add(SendBack())
     .Else()
          .add(StrictAssignVar('msg_out','msg_in'))
     .EndIf()
)  
```

> **_NOTE:_**  The parentheses at the first and last line are to save us from putting a `\` at the end of each line. 

### d) Create a FlowSelector

So far, we described "what to do". Now, it is time to specify which packets are subject to this processing by creating a `FlowSelector`.

The first argument defines the kind of packets we want to deal with. These supported header stacks are defined by the template.

The second argument describes additional filtering rules. We require that the UDP packet's destination port is 5555 and its length is 8+3 (UDP header + payload).

Finally, we provide a flow processor for the selected packets. It is the previously created `fp` in our case.

```python
fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5555),(UdpLen,8+13)],
        fp
    )
```

### e) Put things together

Finally, we patch together our components using a `Solution` object. As the last step, we generate our P4 code.

```python
solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('test.p4app')
```

> **_NOTE:_**  This patching together is more relevant when we have many components sharing the same stateful elements.

## 5. Run the code generator

Just run our previously created Python script.

```bash
python3 codegen.py
```

## 6. Build

We compile our P4 code using the compiler provided by p4app.

```bash
sudo p4app/p4app build test.p4app
```

## 7. Run

You can run your code using p4app as well. It will start a mininet with 2 hosts connected by a P4 switch.

```bash
sudo p4app/p4app run test.p4app
```

## 8. Test

To observe the correct behaviour of our simple P4RROT solution, we need to install netcat and configure the network according to our needs.

```bash
sudo p4app/p4app exec apt install -y netcat
sudo p4app/p4app exec m h1 ifconfig h1-eth0 10.0.0.1/24
sudo p4app/p4app exec m h2 ifconfig h2-eth0 10.0.0.2/24
```

Then, we start a netcat server and client using UDP and appropriate port in different terminals.


```bash
# server
sudo p4app/p4app exec m h2 nc -ul -k -v -p 5555
```

```bash
# client
sudo p4app/p4app exec m h1 nc -u 10.0.0.2 5555
```

Finally, let's send some data to the server. 
If we type 'cat' or 'abcdef012345' it behaves like a normal netcat client-server setup.
However, If we send 'Hello World!', we get an immediate response from the switch saying HELLO. 

Good P4RROT! :)

> **_NOTE:_**  The 'Hello World!' message has never arrived to the server since the very same packet is turned back as a response to the client.