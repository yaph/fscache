#!/usr/bin/env python
# -*- coding: utf-8 -*-
import decimal

from collections import namedtuple
from datetime import datetime

from fscache import fscache


Point = namedtuple('Point', ['x', 'y'])
cache_dir = '.fscache'
cache_file = fscache.path('test_content.json', cache_dir=cache_dir)
content = {
    'set': set('abc'),
    'datetime': datetime.now(),
    'decimal': decimal.Decimal(10),
    'tuple': (1, 2),
    'namedtuple': Point(1, 2)
}


# Create a cache file first.
def test_save():
    fscache.save(cache_file, content, mode='json')
    assert cache_file.exists()


def test_load():
    cached_content = fscache.load(cache_file, mode='json')
    assert content['set'] == set(cached_content['set'])
    assert content['datetime'] == datetime.fromisoformat(cached_content['datetime'])
    assert content['decimal'] == decimal.Decimal(cached_content['decimal'])
    assert content['tuple'] == tuple(cached_content['tuple'])
    assert content['namedtuple'] == Point(*cached_content['namedtuple'])