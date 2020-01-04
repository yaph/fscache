#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from string import ascii_lowercase

from fscache import fscache


data = list(ascii_lowercase)
cache_file = fscache.path('test_fscache.json', cache_dir='.fscache/a/a/a/')


def test_split_id():
    tests = [
        ('https://www.youtube.com/watch?v=HEOxdMWxIBM', (['https', 'www.youtube.com'], 'watch?v=HEOxdMWxIBM')),
        ('https://ramiro.org/vis/index.html', (['https', 'ramiro.org', 'vis'], 'index.html'))
    ]
    for t in tests:
        assert fscache.split_id(t[0], '/') == t[1]


def test_slugify():
    tests = [
        ('/path/to/data.json', 'path-to-data.json'),
        ('Gómez', 'Gómez'),
        ('https://ramiro.org/index.html', 'https-ramiro.org-index.html'),
        ('https/ramiro.org/index.html', 'https-ramiro.org-index.html'),
    ]
    for t in tests:
        assert fscache.slugify(t[0]) == t[1]


def test_save():
    fscache.save(cache_file, data, encoding='json')
    assert cache_file.exists()


def test_load():
    assert fscache.load(cache_file, encoding='json') == data