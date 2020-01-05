# fscache

**fscache** is a Python package for caching data in the file system.

## Installation

```sh
pip install fscache
```

## Usage

```python
import requests
from fscache import fscache

url = 'https://example.com/index.html'
cache_file = fscache.path(url, cache_dir='.fscache')

if fscache.valid(cache_file, lifetime=3600):
    content = fscache.load(cache_file)
    # Do something with content
else:
    content = requests.get(url).text
    # Save content in .fscache/https/example.com/index.html
    fscache.save(cache_file, content)
```

## License

[MIT](LICENSE) © [Ramiro Gómez](https://ramiro.org/)