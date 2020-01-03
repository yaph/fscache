#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from string import ascii_lowercase
import fscache


data = list(ascii_lowercase)
cache_file = fscache.path('test_fscache.json', cache_dir='.fscache/a/a/a/')


def test_save():
    fscache.save(cache_file, json.dumps(data), encoding='json')
    assert cache_file.exists()


def test_load():
    assert fscache.load(cache_file, encoding='json') == data