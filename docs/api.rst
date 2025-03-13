API Reference
=============

.. automodule:: udataclasses

   Alternative implementation of :py:mod:`dataclasses`.

.. autodecorator:: dataclass

   Refer to the documentation for :py:func:`dataclasses.dataclass`.

.. autofunction:: asdict

   Refer to the documentation for :py:func:`dataclasses.asdict`

.. autofunction:: astuple

   Refer to the documentation for :py:func:`dataclasses.astuple`

.. autofunction:: field

   Refer to the documentation for :py:func:`dataclasses.field`.

.. autofunction:: fields

   Refer to the documentation for :py:func:`dataclasses.fields`.

.. autofunction:: is_dataclass

   Refer to the documentation for :py:func:`dataclasses.is_dataclass`.

.. autofunction:: make_dataclass

   Refer to the documentation for :py:func:`dataclasses.make_dataclass`.

.. autofunction:: replace

   Refer to the documentation for :py:func:`dataclasses.replace`.

.. autoexception:: FrozenInstanceError

   Refer to the documentation for :py:class:`dataclasses.FrozenInstanceError`.

.. autoclass:: Field()

   .. autoattribute:: name
   .. autoattribute:: type
      :no-value:

      This attribute only exists for compatibility with the official Python
      implementation. udataclasses does not know the type of fields and this
      simple has the value :py:class:`object`.

   .. autoattribute:: default
   .. autoattribute:: default_factory
   .. autoattribute:: init
   .. autoattribute:: repr
   .. autoattribute:: hash
   .. autoattribute:: compare

.. autodoc doesn't pick up the docstring for this attribute correctly, so we
   manually document it here.
.. py:data:: MISSING

   Sentinel default value for fields without a default value.

   Refer to the documentation for :py:data:`dataclasses.MISSING`.
