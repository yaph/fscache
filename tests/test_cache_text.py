#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fscache import fscache


cache_dir = '.fscache'
cache_file = fscache.path('test_content.txt', cache_dir=cache_dir)
content = 'abc'


# Create a cache file first.
def test_save():
    fscache.save(cache_file, content)
    assert cache_file.exists()


def test_valid():
    assert fscache.valid(cache_file, lifetime=3600)


def test_load():
    assert fscache.load(cache_file) == content