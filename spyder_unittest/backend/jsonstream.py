# -*- coding: utf-8 -*-
#
# Copyright © 2013 Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
r"""
Reader and writer for sending stream of python objects using JSON.

These classes can be used to send Python objects (specifically, ints, floats,
strings, bools, lists, dictionaries or None) over a text stream. Partially
received objects are correctly handled.

Since multiple JSON-encoded objects cannot simply concatenated (i.e., JSON is
not a framed protocol), every object is sent over the text channel in the
format "N \n s \n", where the string s is its JSON encoding and N is the length
of s.
"""

# Standard library imports
import json


class JSONStreamWriter:
    """
    Writer for sending stream of python objects using JSON.

    This class can be used to send a stream of python objects over a text
    stream using JSON. It is the responsibility of the caller to open and
    close the stream.

    Attributes
    ----------
    stream : TextIOBase
        text stream that the objects are sent over.
    """

    def __init__(self, stream):
        """Constructor."""
        self.stream = stream

    def write(self, obj):
        """
        Write Python object to the stream.

        Arguments
        ---------
        obj : object
            Object to be written. The type should be supported by JSON (i.e.,
            int, float, str, bool, list, dict or None).
        """
        txt = json.dumps(obj)
        self.stream.write(str(len(txt)) + '\n')
        self.stream.write(txt + '\n')


class JSONStreamReader:
    """
    Reader for sending stream of Python objects using JSON.

    This class is used to receive a stream sent by JSONStreamWriter.

    Attributes
    ----------
    buffer : str
       Text encoding an object that has not been completely received yet.
    """

    def __init__(self):
        """Constructor."""
        self.buffer = ''

    def consume(self, txt):
        """
        Decode given text and return list of objects encoded in it.

        If only a part of the encoded text of an object is passed, then it is
        stored and combined with the remainder in the next call.
        """
        index = 0
        res = []
        txt = self.buffer + txt
        while index < len(txt):
            end_of_line1 = txt.find('\n', index)
            len_encoding = int(txt[index:end_of_line1])
            if end_of_line1 + len_encoding + 2 > len(txt):  # 2 for two \n
                break
            encoding = txt[end_of_line1 + 1:end_of_line1 + len_encoding + 1]
            res.append(json.loads(encoding))
            index = end_of_line1 + len_encoding + 2
        self.buffer = txt[index:]
        return res