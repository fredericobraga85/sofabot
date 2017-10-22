import requests



def get_url(url, params):
    try:
        import urlparse
        from urllib import urlencode
    except:  # For Python 3
        import urllib.parse as urlparse
        from urllib.parse import urlencode

    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urlencode(query)
    u = urlparse.urlunparse(url_parts)

    print 'Request GET to', u
    r = requests.get(u)

    return r.content
