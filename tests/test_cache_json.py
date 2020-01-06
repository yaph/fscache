#!/usr/bin/env python
# -*- coding: utf-8 -*-
import decimal
import uuid

from datetime import datetime

from fscache import fscache


cache_dir = '.fscache'
cache_file = fscache.path('test_content.json', cache_dir=cache_dir)
content = {
    'bytes': b'abc',
    'datetime': datetime.now(),
    'decimal': decimal.Decimal(10),
    'set': set('abc'),
    'uuid': uuid.uuid1()
}


# Create a cache file first.
def test_save():
    fscache.save(cache_file, content, mode='json')
    assert cache_file.exists()


def test_load():
    cached_content = fscache.load(cache_file, mode='json')
    assert content['bytes'] == cached_content['bytes'].encode()
    assert content['datetime'] == datetime.fromisoformat(cached_content['datetime'])
    assert content['decimal'] == decimal.Decimal(cached_content['decimal'])
    assert content['set'] == set(cached_content['set'])
    assert content['uuid'] == uuid.UUID(cached_content['uuid'])