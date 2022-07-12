# fmt: off
from datetime import timedelta
from requests_cache import CachedSession
session_cached = CachedSession(
    'demo_cache',                      # ~/.cache/demo_cache.sqlite
    use_cache_dir=True,                # Save files in the default user cache dir
    cache_control=True,                # Use Cache-Control headers for expiration, if available
                                       #    some website, have 'Cache-Control': 'private, max-age=0'
    expire_after=timedelta(days=1),    # Otherwise expire responses after one day
    allowable_methods=['GET', 'POST'], # Cache POST requests to avoid sending the same data twice
    allowable_codes=[200, 400],        # Cache 400 responses as a solemn reminder of your failures
    ignored_parameters=['api_key'],    # Don't match this param or save it in the cache
    match_headers=True,                # Match all request headers
    stale_if_error=True,               # In case of request errors, use stale cache data if possible
  )
session_cached.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'})

import requests
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'})

def getz(url):
  return session.get(url, stream=True) 

def getc(url):
  return session_cached.get(url)

def clear():
  return  session_cached.cache.clear()

if __name__ == '__main__':
  for i in range(60):
    session_cached.get('https://httpbin.org/delay/1')

  with session_cached.cache_disabled():
    print("cache disabled")
    for i in range(10):
      session_cached.get('http://httpbin.org/delay/1')
