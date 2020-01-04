# -*- coding: utf-8 -*-
# A Python package for caching data in the file system.
import json
import re

import jsonpickle

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from appdirs import user_cache_dir


__all__ = ['path', 'load', 'save', 'valid']


re_forbidden = re.compile(r'[^\.\w]+')


def slugify(s: str) -> str:
    """Return string with forbidden characters replaced by hyphens.

    Consecutive forbidden characters are replaced with a single hyphen.
    Leading and trailing whitespace and hyphens are stripped.
    Different input strings may result in the same output.
    """
    return re.sub(re_forbidden, '-', s.strip()).strip('-')


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
        underscore and period. Other characters will be replaced with a hyphen, which can result in name collisions.

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
        parts = list(filter(None, cache_id.split(split_char)))
        sub_dirs = [slugify(d) for d in parts[:-1]]
        cache_id = parts[-1]
        # Call `as_posix` so `cache_dir` stays a string.
        cache_dir = Path(cache_dir, *sub_dirs).as_posix()

    cache_path = Path(cache_dir, slugify(cache_id))
    if create_dirs:
        cache_path.parent.mkdir(exist_ok=True, parents=True)

    return cache_path


def load(cache_file: Path, *, mode: str = None, unsafe: bool = False):
    """Return the content of the cache file.

    Parameters
    ----------
    cache_file
        The Path object representing the cache file.

    mode
        If `mode` is not set a text file is assumed. Set `mode` to `bytes` for binary files like images or PDF files.
        Set to `json` to deserialize the file content into a Python object.

    unsafe
        This only applies to `json` mode. If `False` Python's built-in `json` module will be used. If `True` content
        is decoded using `jsonpickle` which can execute arbitrary Python code.
    """
    if mode == 'bytes':
        return cache_file.read_bytes()

    content = cache_file.read_text()
    if mode == 'json':
        if unsafe:
            content = jsonpickle.decode(content)
        else:
            content = json.loads(content)

    return content


def save(cache_file: Path, data: Any, *, mode: str = None, unsafe: bool = False):
    """Save data in cache file.

    Parameters
    ----------
    cache_file
        The Path object representing the cache file.

    mode
        If `mode` is not set a text file is assumed. Set `mode` to `bytes` for binary files like images or PDF files.
        Set to `json` to serialize the data.

    unsafe
        This only applies to `json` mode. If `False` Python's built-in `json` module will be used. If `True` content
        is encoded using `jsonpickle`. This is useful when the data contains Python objects like datetimes and sets.
    """
    if mode == 'bytes':
        cache_file.write_bytes(data)
    else:
        content = None
        if mode == 'json':
            if unsafe:
                content = jsonpickle.encode(data)
            else:
                content = json.dumps(data)
        cache_file.write_text(content)


def valid(cache_file: Path, lifetime: int = None) -> bool:
    """Check whether cache file is valid.

    Parameters
    ----------
    cache_file
        The Path object representing the cache file. Returns `False` if cache file doesn't exist.
    lifetime
        An integer value in seconds. If not set and the cache file exists returns `True`. Otherwise the lifetime is compared to
        the file modification time.
    """

    if not cache_file.exists():
        return False

    if lifetime is None:
        return True

    mtime = datetime.fromtimestamp(cache_file.lstat().st_mtime)
    if datetime.now() - timedelta(seconds=lifetime) < mtime:
        return True

    return False