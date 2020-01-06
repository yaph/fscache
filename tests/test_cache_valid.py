#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fscache import fscache


cache_dir = '.fscache'
cache_file = fscache.path('test_valid.txt', cache_dir=cache_dir)
cache_file_not_exists = fscache.path('test_valid_not_exists.txt')
content = 'abc'


# Create a cache file first.
def test_save():
    fscache.save(cache_file, content)
    assert cache_file.exists()


def test_valid_not_exists():
    assert fscache.valid(cache_file_not_exists) is False


def test_valid_with_lifetime():
    assert fscache.valid(cache_file, lifetime=3600)


def test_valid_with_lifetime_zero():
    assert fscache.valid(cache_file, lifetime=0) is False


def test_valid_without_lifetime():
    assert fscache.valid(cache_file)


def test_load():
    assert fscache.load(cache_file) == content