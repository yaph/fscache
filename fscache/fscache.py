# -*- coding: utf-8 -*-
"""A Python package for caching data in the file system."""

import json
import re

from datetime import datetime, timedelta
from pathlib import Path
from string import ascii_lowercase
from typing import Any

from .encoder import JSONEncoder


re_forbidden = re.compile(r'[^\.\w-]+')
re_ws = re.compile(r'\s+')
re_hyphen = re.compile(r'-+')


def slugify(s: str) -> str:
    """Return string with forbidden characters replaced with hyphens.

    Leading and trailing whitespace is stripped.
    Different input strings may result in the same output.
    """

    return re.sub(re_forbidden, ' ', s.strip()).strip().replace(' ', '-')


def create_id(s: str, sep: str = '/') -> str:
    """Create a cache ID for given string that is a valid file path.

    Set `sep` to a valid directory separator to create sub directories as they occur in the string.
    """
    if sep and sep in s:
        return sep.join([slugify(part) for part in s.split(sep) if part])
    return slugify(s)


def path(
        cache_id: str,
        *,  # keyword-only arguments
        alpha_index: str = '',
        cache_dir: str = '',
        create_dirs: bool = True) -> Path:
    """Return a pathlib.Path object pointing to the cache file.

    Parameters
    ----------
    cache_id
        A unique string for identifying cache files. It is used as the file name and should only contain alphanumeric
        characters, underscore and period. If it contains the directory separator `/` sub directories will be created
        appropriately. Other characters will be replaced with a hyphen, which can result in name collisions.

    alpha_index
        If set to `name` this will create an alphabetical directory index, which is useful for adding more structure
        when storing many cache files, that have meaningful names mostly starting with ASCII letters. The first
        character of the file name will be used to create an additional directory to store the file in. Files that
        don't start with an ASCII letter are stored in the `_` directory.

    cache_dir
        An optional base directory for storing cache files. If set and the directory does not exist an exception is
        raised. Otherwise files will be stored in the `.fscache` directory in the user's home directory.

    create_dirs
        An optional flag to control directory creation. By default directories determined from the cache ID will be
        created as needed. Set this to `False` to prevent directory creation. Useful if you know the cache directory
        exists and for tests.
    """

    if cache_dir:
        p_cache = Path(cache_dir).expanduser()
        if not p_cache.exists():
            raise FileNotFoundError(f'Cache directory does not exist: {p_cache.absolute()}')
    else:
        p_cache = Path(Path.home(), '.fscache')

    p_cache = p_cache / create_id(cache_id)

    if alpha_index == 'name':
        first = p_cache.name.lower()[0]
        if first not in ascii_lowercase:
            first = '_'
        p_cache = p_cache.parent.joinpath(first, p_cache.name)

    if create_dirs:
        p_cache.parent.mkdir(exist_ok=True, parents=True)

    return p_cache


def load(cache_file: Path, *, mode: str = '', unsafe: bool = False):
    """Return the content of the cache file.

    Parameters
    ----------
    cache_file
        The Path object representing the cache file.

    mode
        If `mode` is not set a text file is assumed. Set `mode` to `binary` for binary files like images or PDF files.
        Set to `json` to deserialize the file content into a Python object.
    """
    if mode == 'binary':
        return cache_file.read_bytes()

    content = cache_file.read_text()
    if mode == 'json':
        content = json.loads(content)

    return content


def save(cache_file: Path, content: Any, *, mode: str = ''):
    """Save data in cache file.

    Parameters
    ----------
    cache_file
        The Path object representing the cache file.

    content
        The content to store in the cache file.

    mode
        If `mode` is not set a text file is assumed. Set `mode` to `binary` for binary files like images or PDF files.
        Set to `json` to serialize the data.
    """
    if mode == 'binary':
        cache_file.write_bytes(content)
    else:
        if mode == 'json':
            content = json.dumps(content, cls=JSONEncoder)
        cache_file.write_text(content)


def valid(cache_file: Path, lifetime: int | None = None) -> bool:
    """Check whether cache file is valid.

    Parameters
    ----------
    cache_file
        The Path object representing the cache file. Returns `False` if cache file doesn't exist.
    lifetime
        An integer value in seconds. If not set and the cache file exists returns `True`. Otherwise the lifetime is
        compared to the file modification time.
    """

    if not cache_file.exists():
        return False

    if lifetime is None:
        return True

    mtime = datetime.fromtimestamp(cache_file.lstat().st_mtime)
    if datetime.now() - timedelta(seconds=lifetime) < mtime:
        return True

    return False