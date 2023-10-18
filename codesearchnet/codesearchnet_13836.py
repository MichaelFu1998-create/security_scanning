def open(url, wait=10):

    """ Returns a connection to a url which you can read().

    When the wait amount is exceeded, raises a URLTimeout.
    When an error occurs, raises a URLError.
    404 errors specifically return a HTTP404NotFound.

    """

    # If the url is a URLParser, get any POST parameters.
    post = None
    if isinstance(url, URLParser) and url.method == "post":
        post = urllib.urlencode(url.query)

    # If the url is a URLParser (or a YahooResult or something),
    # use its string representation.
    url = str(url)

    # Use urllib instead of urllib2 for local files.
    if os.path.exists(url):
        return urllib.urlopen(url)

    else:
        socket.setdefaulttimeout(wait)
        try:
            #connection = urllib2.urlopen(url, post)
            request = urllib2.Request(url, post, {"User-Agent": USER_AGENT, "Referer": REFERER})
            if PROXY:
                p = urllib2.ProxyHandler({PROXY[1]: PROXY[0]})
                o = urllib2.build_opener(p, urllib2.HTTPHandler)
                urllib2.install_opener(o)
            connection = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            if e.code == 401: raise HTTP401Authentication
            if e.code == 403: raise HTTP403Forbidden
            if e.code == 404: raise HTTP404NotFound
            raise HTTPError
        except urllib2.URLError, e:
            if e.reason[0] == 36: raise URLTimeout
            raise URLError

    return connection