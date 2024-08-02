# tibero/pyodbc.py
# Copyright (C) 2005-2012 the SQLAlchemy authors and contributors <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""
Support for TmaxSoft Tibero via pyodbc.

pyodbc is available at:
    http://pypi.python.org/pypi/pyodbc/

Connecting
^^^^^^^^^^
Examples of pyodbc connection string URLs:
* ``tibero+pyodbc://mydsn`` - connects using the specified DSN named ``mydsn``.
"""
import os

from .base import TiberoExecutionContext, TiberoDialect
from sqlalchemy.connectors.pyodbc import PyODBCConnector
from sqlalchemy.types import BLOB
from sqlalchemy.types import CLOB
from sqlalchemy.types import NCHAR
from sqlalchemy.types import TIMESTAMP

from .types import NCLOB


class TiberoExecutionContext_pyodbc(TiberoExecutionContext):
    pass


class TiberoDialect_pyodbc(PyODBCConnector, TiberoDialect):
    pyodbc_driver_name = "Tibero"
    execution_ctx_cls = TiberoExecutionContext_pyodbc
    colspecs = TiberoDialect.colspecs
    supports_statement_cache = True
    bind_typing = 2

    @classmethod
    def dbapi(cls):
        return PyODBCConnector.dbapi()

    def __init__(
        self,
        auto_convert_lobs=True,
        coerce_to_decimal=True,
        arraysize=50,
        encoding_errors=None,
        threaded=None,
        **kwargs,
    ):
        os.environ.update([
            # Tibero takes client-side character set encoding from the environment.
            ('TB_NLS_LANG', 'UTF8'),
            # This prevents unicode from getting mangled by getting encoded into the
            # potentially non-unicode database character set.
            ('TBCLI_WCHAR_TYPE', 'UCS2'),
        ])

        TiberoDialect.__init__(self, **kwargs)
        self.arraysize = arraysize
        self.encoding_errors = encoding_errors
        if encoding_errors:
            self._cursor_var_unicode_kwargs = {
                "encodingErrors": encoding_errors
            }
        if threaded is not None:
            self._cx_oracle_threaded = threaded
        self.auto_convert_lobs = auto_convert_lobs
        self.coerce_to_decimal = coerce_to_decimal
        self.include_set_input_sizes = {
            NCLOB,
            CLOB,
            NCHAR,
            BLOB,
            TIMESTAMP,
        }
