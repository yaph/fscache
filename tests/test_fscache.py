#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from string import ascii_lowercase

from appdirs import user_cache_dir

from fscache import fscache

cache_dir = '.fscache'
data = list(ascii_lowercase)
cache_file = fscache.path('test_fscache.json', cache_dir=cache_dir)


# Create a cache file first.
def test_save():
    fscache.save(cache_file, data, mode='json')
    assert cache_file.exists()


def test_slugify():
    tests = [
        ('/path/to/data.json', 'path-to-data.json'),
        ('Gómez', 'Gómez'),
        ('https://ramiro.org/index.html', 'https-ramiro.org-index.html'),
        ('https/ramiro.org/index.html', 'https-ramiro.org-index.html'),
    ]
    for t in tests:
        assert fscache.slugify(t[0]) == t[1]


def test_path_default_cache_dir():
    assert fscache.path('file.txt', create_dirs=False).as_posix() == f'{user_cache_dir("fscache")}/file.txt'


def test_path_split_char():
    tests = [
        ('https://www.youtube.com/watch?v=HEOxdMWxIBM', f'{cache_dir}/https/www.youtube.com/watch-v-HEOxdMWxIBM'),
        ('https://ramiro.org/vis/index.html', f'{cache_dir}/https/ramiro.org/vis/index.html')
    ]
    for t in tests:
        assert fscache.path(t[0], cache_dir=cache_dir, create_dirs=False, split_char='/').as_posix() == t[1]


# Run these last
def test_valid():
    assert fscache.valid(cache_file, lifetime=3600)


def test_load():
    assert fscache.load(cache_file, mode='json') == data