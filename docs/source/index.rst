.. P4RROT documentation master file, created by
   sphinx-quickstart on Thu Mar 31 11:10:35 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to P4RROT's documentation!
==================================

Generating P4 Code for the Application Layer
--------------------------------------------

Motivation
~~~~~~~~~~

Throughput and latency-critical applications (e.g. processing sensor data, robot control, or monitoring stock market streams) can often benefit if computations are performed close to the client. Performing these computations in the data plane can help us take it to the next level.

P4 is excellent data plane programming language, and we all love it. However, it wasn't meant to implement application-layer tasks. Thus, offloading server-functionality can be challenging.

P4RROT is a code generator that helps programmers overcome certain limitations and write shorter and easier-to-read code.

Supported targets
~~~~~~~~~~~~~~~~~

P4RROT is a very young project. The current code base supports both the BMv2 and the Netronome NFP.

We plan to add Tofino specific elements as well.


.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   getting_started/internal_workings.rst
   getting_started/install_guide.rst
   getting_started/hello_world.rst
   getting_started/complex_example.rst

.. toctree::
   :maxdepth: 2
   :caption: API Documentation:

   core/index
   v1model/index
   tofino/index

   api_summary


.. toctree::
   :maxdepth: 2
   :caption: Extending P4RROT:

   extending/command
   extending/stateful
   extending/template

.. toctree::
   :maxdepth: 2
   :caption: Contributors:

   contributors


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
