# -*- coding: utf-8 -*-
# A Python package for caching data in the file system.
import json
import re

import jsonpickle

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Tuple

from appdirs import user_cache_dir


__all__ = ['path', 'load', 'save', 'valid']


re_forbidden = re.compile(r'[^\.\w-]+')


def slugify(s: str) -> str:
    return re.sub(re_forbidden, '-', s.strip()).strip('-')


def split_id(cache_id: str, sep: str) -> Tuple[list, str]:
    parts = list(filter(None, cache_id.split(sep)))
    sub_dirs = [slugify(d) for d in parts[:-1]]
    return sub_dirs, parts[-1]


def path(
    cache_id: str,
    *,  # keyword-only arguments
    cache_dir: str = '',
    create_dirs: bool = True,
    split_char: str = '') -> Path:
    """Return a pathlib.Path object pointing to the cache file.

    Parameters
    ----------
    cache_id
        A unique string for identifying cache files. It is used as the file name and should only contain alphanumeric characters,
        hyphen, underscore and period. Other characters will be replaced with hyphens, which can result in name collisions.

    cache_dir
        An optional string to specify the directory for storing cache files. If set and the directory does not exist an exception
        is raised. If not set files will be stored in the `fscache` directory within the operating system user cache directory.

    create_dirs
        An optional flag to control directory creation. By default the cache directory and all parents will be created as needed.
        Set this to `False` to prevent directory creation. Useful if you know the cache directory exists and for tests.

    split_char
        An optional string that will be used to split the `cache_id` into parts, which are turned into sub directories and only
        the last part is the file name. If you use URLs as cache IDs and `/` as `split_char`, sub directories for the scheme,
        host and path directories will be created.
    """

    if cache_dir and not Path(cache_dir).exists():
        raise FileNotFoundError('Cache directory does not exist: ' + cache_dir)

    if not cache_dir:
        cache_dir = user_cache_dir('fscache')

    if split_char and split_char in cache_id:
        sub_dirs, cache_id = split_id(cache_id, split_char)
        # Call `as_posix` so `cache_dir` stays a string.
        cache_dir = Path(cache_dir, *sub_dirs).as_posix()

    cache_path = Path(cache_dir, slugify(cache_id))
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


def valid(cache_file: Path, lifetime: int = None) -> bool:
    if not cache_file.exists():
        return False

    if lifetime is None:
        return True

    mtime = datetime.fromtimestamp(cache_file.lstat().st_mtime)
    if datetime.now() - timedelta(seconds=lifetime) < mtime:
        return True

    return False