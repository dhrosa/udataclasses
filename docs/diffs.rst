.. |dataclasses| replace:: :py:mod:`dataclasses`
.. |udataclasses| replace:: :py:mod:`udataclasses`

Differences between |udataclasses| and |dataclasses|
====================================================

Field attributes must have values
---------------------------------

In MicroPython and CircuitPython, fhe following code does **not** work:

.. code:: python

   from udataclasses import dataclass

   @dataclass
   class Product:
       quantity: int

The attribute must be given a default value:

.. code:: python

   from udataclasses import dataclass

   @dataclass
   class Product:
       quantity: int = 0

Or you can use :py:func:`field()<udataclasses.field>` with no arguments to
indicate that the field has no default value:

.. code:: python

   from udataclasses import dataclass, field

   @dataclass
   class Product:
       quantity: int = field()

.. dropdown:: Explanation

   MicroPython accepts type annotations as valid syntax, but discards them.
   There is no way in the runtime to access type annotations, e.g. using
   :py:func:`inspect.get_annotations` in standard Python.

   A line that gives an attribute a type annotation without providing a value is
   effectively the same as an empty line in MicroPython. Take a look at the
   following MicroPython REPL session:

   .. code:: pycon

      >>> class C:
      ...     a: int
      ...     b: int = 0
      ...
      >>> C.__dict__.keys()
      dict_keys(['__module__', 'b', '__qualname__'])

   The code knows about the attribute ``b``, but there is no mention of ``a``.
   Because of this, |udataclasses| fields have to be assigned a value in order
   for us to be able to detect the field.


|field_type| has the wrong value
--------------------------------

MicroPython does not store type annotations anywhere, so there is no way for
|udataclasses| to know the correct type for a field. Instead, |field_type| is
hardcoded to :py:class:`object`.

.. |field_type| replace:: :py:attr:`Field.type <udataclasses.Field.type>`

Missing features from |dataclasses|
-----------------------------------

We don't currently support every feature that the standard |dataclasses| has.
These are a work in progress. We aim to have feature parity with at least Python
3.9's version of |dataclasses| where possible. See
https://github.com/dhrosa/udataclasses/issues for progress on these missing
features.
