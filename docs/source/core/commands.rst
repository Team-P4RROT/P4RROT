Stateless Commands
==================

Assignment
----------

.. autoclass:: p4rrot.core.commands.AssignConst
   :members:
   :special-members:

.. autoclass:: p4rrot.core.commands.StrictAssignVar
   :members:
   :special-members:

.. autoclass:: p4rrot.core.commands.CastVar
   :members:
   :special-members:


Arithmetic operations
---------------------

.. autoclass:: p4rrot.core.commands.Increment
   :members: __init__

.. autoclass:: p4rrot.core.commands.Decrement
   :members: __init__

.. autoclass:: p4rrot.core.commands.StrictAddition
   :members: __init__

.. autoclass:: p4rrot.core.commands.StrictSubtraction
   :members: __init__


Comparators
-----------

.. autoclass:: p4rrot.core.commands.GreaterThan
   :members: __init__

.. autoclass:: p4rrot.core.commands.LessThan
   :members: __init__

.. autoclass:: p4rrot.core.commands.Equals
   :members: __init__

Logical operations
------------------

.. autoclass:: p4rrot.core.commands.LogicalAnd
   :members: __init__

.. autoclass:: p4rrot.core.commands.LogicalOr
   :members: __init__

.. autoclass:: p4rrot.core.commands.LogicalNot
   :members: __init__

Control-flow statements
-----------------------

If-Else statement
~~~~~~~~~~~~~~~~~

A simple example If-Else statement:

.. code-block:: python

   fp.add(GreaterThan('x','a','b'))\
     .add(If('x'))\
            .add(Increment('a',5))\
            .add(Increment('b',7))\
         .Else()\
            .add(Decrement('a',6))\
            .add(Decrement('b',8))\
         .EndIf()\

A more complex and complete example can be found in the test_builds/08_complex_if.test folder.

.. autoclass:: p4rrot.core.commands.If
   :members: __init__

.. autoclass:: p4rrot.core.commands.ThenBlock
   :members: Else, EndIf

.. autoclass:: p4rrot.core.commands.ElseBlock
   :members: EndIf


Switch statement
~~~~~~~~~~~~~~~~
