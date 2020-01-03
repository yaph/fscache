# -*- coding: utf-8 -*-
# A Python package for caching data in the file system.
import json

import jsonpickle

from datetime import datetime, timedelta
from pathlib import Path

from appdirs import user_cache_dir
from slugify import slugify


def split_id(cache_id, sep):
    parts = list(filter(None, cache_id.split(sep)))
    sub_dirs = [slugify(d) for d in parts[:-1]]
    return sub_dirs, parts[-1]


def path(cache_id, cache_dir='', create_dirs=True, split_char='', subdir_levels=0):
    # TODO raise Exception if cache_dir is set but doesn't exist?
    if not cache_dir:
        cache_dir = user_cache_dir('fscache')

    # If you pass a full URL as a cache ID and use `/` as `split_char`, sub directories
    # for the scheme, host, and the path directories will be created.
    if split_char and split_char in cache_id:
        sub_dirs, cache_id = split_id(cache_id, split_char)
        cache_dir = Path(cache_dir, *sub_dirs)

    cache_path = Path(cache_dir, slugify(cache_id))
    if create_dirs:
        cache_path.parent.mkdir(exist_ok=True, parents=True)

    return cache_path


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