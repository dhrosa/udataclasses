.. |dataclasses| replace:: :py:mod:`dataclasses`
.. |decorator| replace:: :py:func:`@dataclass <udataclasses.dataclass>`
.. |field_type| replace:: :py:attr:`Field.type <udataclasses.Field.type>`
.. |fields| replace:: :py:func:`fields <udataclasses.fields>`
.. |field| replace:: :py:func:`field()<udataclasses.field>`
.. |init| replace:: :py:meth:`__init__ <object.__init__>`
.. |repr| replace:: :py:meth:`__repr__ <object.__repr__>`
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
       name: str
       quantity: int

The attributes must either be given a default value, or you can use |field| with
no arguments:

.. code:: python

   from udataclasses import dataclass

   @dataclass
   class Product:
       name: str = field()
       quantity: int = 0

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

.. _field_ordering:

Fields are sorted alphabetically instead of by source order
-----------------------------------------------------------

Methods we generate such as |repr|, and functions such as |fields| sort fields
alphabetically by name, rather than preserving the order in your source code.
For example:

.. code:: python

   from udataclasses import dataclass, field

   @dataclass
   class Product:
       quantity: int = 0
       name: str = field()

   # This prints 'Product(name="bolts", quantity=2)'
   print(Product(quantity=2, name="bolts"))

.. dropdown:: Explanation

   MicroPython does not store class attributes in creation order, so |decorator|
   cannot retain the order of the fields in the order they were listed in the
   user's source code. In order to provide a consistent order, |decorator|
   automatically sorts the field names alphabetically in its output.


|init| arguments are keyword-only
----------------------------------

Classes decorated with |decorator| will not allow passing positional arguments to |init|. For example:

.. code:: python

   from udataclasses import dataclass, field

   @dataclass
   class Product:
       name: str = field()
       quantity: int = 0

   # The commented-out line below raises a TypeError
   # Product("bolts", 2)

   # This next line works however:
   Product(name="bolts", quantity=2)


.. dropdown:: Explanation

   We sort fields :ref:`alphabetically <field_ordering>`. If we allowed
   positional |init| arguments, the order of those arguments would not match the
   field order in your code. Therefore, allowing positional arguments would be
   very error-prone. Instead we only allow arguments to be passed in by keyword,
   which has no ordering constraints.


|field_type| has the wrong value
--------------------------------

MicroPython does not store type annotations anywhere, so there is no way for
|udataclasses| to know the correct type for a field. Instead, |field_type| is
hardcoded to :py:class:`object`.


Missing features from |dataclasses|
-----------------------------------

We don't currently support every feature that the standard |dataclasses| has.
These are a work in progress. We aim to have feature parity with at least Python
3.9's version of |dataclasses| where possible. See
https://github.com/dhrosa/udataclasses/issues for progress on these missing
features.
