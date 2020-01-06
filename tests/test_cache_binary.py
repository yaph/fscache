#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fscache import fscache


cache_dir = '.fscache'
cache_file = fscache.path('test_content.gif', cache_dir=cache_dir)
# Smallest GIF http://probablyprogramming.com/2009/03/15/the-tiniest-gif-ever
content = b'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;'


# Create a cache file first.
def test_save():
    fscache.save(cache_file, content, mode='binary')
    assert cache_file.exists()


def test_load():
    assert fscache.load(cache_file, mode='binary') == content