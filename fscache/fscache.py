# -*- coding: utf-8 -*-
# A Python package for caching data in the file system.
import json

import jsonpickle

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Tuple

from appdirs import user_cache_dir
from slugify import slugify


def split_id(cache_id: str, sep: str) -> Tuple[list, str]:
    parts = list(filter(None, cache_id.split(sep)))
    sub_dirs = [slugify(d) for d in parts[:-1]]
    return sub_dirs, parts[-1]


def slugify_id(cache_id: str) -> str:
    """Slugify `cache_id` retaining file extension."""

    path_id = Path(cache_id)
    if path_id.suffix:
        return slugify(path_id.stem) + path_id.suffix
    return slugify(cache_id)


def path(
    cache_id: str,
    cache_dir: str = '',
    create_dirs: bool = True,
    split_char: str = '',
    subdir_levels: int = 0) -> Path:

    # TODO raise Exception if cache_dir is set but doesn't exist?
    if not cache_dir:
        cache_dir = user_cache_dir('fscache')

    # If you pass a full URL as a cache ID and use `/` as `split_char`, sub directories
    # for the scheme, host, and the path directories will be created.
    if split_char and split_char in cache_id:
        sub_dirs, cache_id = split_id(cache_id, split_char)
        # Call `as_posix` so `cache_dir` stays a string.
        cache_dir = Path(cache_dir, *sub_dirs).as_posix()

    cache_path = Path(cache_dir, slugify_id(cache_id))
    if create_dirs:
        cache_path.parent.mkdir(exist_ok=True, parents=True)

    return cache_path


def load(cache_file: Path, encoding: str = 'text'):
    if encoding == 'text':
        return cache_file.read_text()
    elif encoding == 'json':
        # Don't use jsonpickle for decoding for security concerns.
        return json.loads(cache_file.read_text())
    else:
        return cache_file.read_bytes()


def save(cache_file: Path, data: Any, encoding: str = 'text'):
    if encoding == 'text':
        cache_file.write_text(data)
    elif encoding == 'json':
        cache_file.write_text(jsonpickle.encode(data))
    else:
        cache_file.write_bytes(data)


def valid(cache_file: Path, lifetime: int):
    if not cache_file.exists():
        return False

    mtime = datetime.fromtimestamp(cache_file.lstat().st_mtime)
    if datetime.now() - timedelta(seconds=lifetime) < mtime:
        return True

    return False