# -*- coding: utf-8 -*-
#
# Copyright © 2017 Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
"""Tests for jsonstream.py"""

# Standard library imports
from io import StringIO

# Local imports
from spyder_unittest.backend.jsonstream import (JSONStreamReader,
                                                JSONStreamWriter)


def test_jsonstreamwriter_with_list():
    stream = StringIO()
    writer = JSONStreamWriter(stream)
    writer.write([1, 2])
    assert stream.getvalue() == '6\n[1, 2]\n'


def test_jsonstreamwriter_with_unicode():
    stream = StringIO()
    writer = JSONStreamWriter(stream)
    writer.write('三')
    assert stream.getvalue() == '8\n"\\u4e09"\n'


def test_jsonstreamreader_with_list():
    reader = JSONStreamReader()
    assert reader.consume('6\n[1, 2]\n') == [[1, 2]]


def test_jsonstreamreader_with_unicode():
    reader = JSONStreamReader()
    assert reader.consume('8\n"\\u4e09"\n') == ['三']


def test_jsonstreamreader_with_partial_frames():
    reader = JSONStreamReader()
    txt = '1\n2\n' * 3
    assert reader.consume(txt[:2]) == []
    assert reader.consume(txt[2:-2]) == [2, 2]
    assert reader.consume(txt[-2:]) == [2]


def test_isonsteamreader_writer_integration():
    stream = StringIO()
    writer = JSONStreamWriter(stream)
    reader = JSONStreamReader()
    writer.write([1, 2])
    writer.write({'a': 'b'})
    assert reader.consume(stream.getvalue()) == [[1, 2], {'a': 'b'}]