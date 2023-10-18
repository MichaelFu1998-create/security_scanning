def relative_to_full(url, example_url):
    """
    Given a url which may or may not be a relative url, convert it to a full
    url path given another full url as an example
    """
    if re.match('https?:\/\/', url):
        return url
    domain = get_domain(example_url)
    if domain:
        return '%s%s' % (domain, url)
    return url