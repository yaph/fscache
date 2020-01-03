# -*- coding: utf-8 -*-
# A Python package for caching data in the file system.
# TODO use https://github.com/ActiveState/appdirs
import json

import jsonpickle

from datetime import datetime, timedelta
from pathlib import Path

from slugify import slugify


def path(cache_id, cache_dir='', subdir_levels=0):
    # TODO if the cache_id contains slashes, create subdirs.
    # TODO slugify cache_id
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(exist_ok=True, parents=True)
    return Path(cache_dir, cache_id)


def load(cache_file, encoding='text'):
    if encoding == 'text':
        return cache_file.read_text()
    elif encoding == 'json':
        # Don't use jsonpickle for decoding for security concerns.
        return json.loads(cache_file.read_text())
    else:
        return cache_file.read_bytes()


def save(cache_file, data, encoding='text'):
    if encoding == 'text':
        cache_file.write_text(data)
    elif encoding == 'json':
        cache_file.write_text(jsonpickle.encode(data))
    else:
        cache_file.write_bytes(data)


def valid(cache_file, lifetime):
    if not cache_file.exists():
        return False

    mtime = datetime.fromtimestamp(cache_file.lstat().st_mtime)
    if datetime.now() - timedelta(seconds=lifetime) < mtime:
        return True

    return False