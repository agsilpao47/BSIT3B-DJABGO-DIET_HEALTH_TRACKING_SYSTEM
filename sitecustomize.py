"""Compatibility shim for Django on Python 3.14+.

Python 3.14 changed how ``super()`` interacts with ``copy.copy()``; Django's
``BaseContext.__copy__`` calls ``copy(super())`` which crashes under this runtime.
Patch it as soon as Python starts so the project can continue to render templates.
"""

from __future__ import annotations

from django.template import context as django_context


def _base_context_copy_compat(self):
    duplicate = object.__new__(type(self))
    duplicate.__dict__ = self.__dict__.copy()
    duplicate.dicts = self.dicts[:]
    return duplicate


django_context.BaseContext.__copy__ = _base_context_copy_compat
