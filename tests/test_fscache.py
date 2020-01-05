#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
        ('a - b', 'a-b'),
        ('/path/to/data.json', 'path-to-data.json'),
        ('Gómez', 'Gómez'),
        ('https://ramiro.org/index.html', 'https-ramiro.org-index.html'),
        ('https/ramiro.org/index.html', 'https-ramiro.org-index.html'),
    ]
    for t in tests:
        assert fscache.slugify(t[0]) == t[1]


def test_create_id():
    tests = [
        ('https://www.youtube.com/watch?v=HEOxdMWxIBM', 'https/www.youtube.com/watch-v-HEOxdMWxIBM'),
        ('https://ramiro.org/vis/index.html', 'https/ramiro.org/vis/index.html')
    ]
    for t in tests:
        assert fscache.create_id(t[0]) == t[1]


def test_path_alpha_index():
    tests = [
        ('alpha.txt', f'{cache_dir}/a/alpha.txt'),
        ('álpha.txt', f'{cache_dir}/_/álpha.txt'),
        ('0-zero.txt', f'{cache_dir}/_/0-zero.txt')
    ]
    for t in tests:
        assert fscache.path(t[0], alpha_index='name', cache_dir=cache_dir, create_dirs=False).as_posix() == t[1]


def test_path_default_cache_dir():
    assert fscache.path('file.txt', create_dirs=False).as_posix() == f'{user_cache_dir("fscache")}/file.txt'


# Run these last
def test_valid():
    assert fscache.valid(cache_file, lifetime=3600)


def test_load():
    assert fscache.load(cache_file, mode='json') == data