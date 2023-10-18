def url_as_file(url, ext=None):
    """
        Context manager that GETs a given `url` and provides it as a local file.

        The file is in a closed state upon entering the context,
        and removed when leaving it, if still there.

        To give the file name a specific extension, use `ext`;
        the extension can optionally include a separating dot,
        otherwise it will be added.

        Parameters:
            url (str): URL to retrieve.
            ext (str, optional): Extension for the generated filename.

        Yields:
            str: The path to a temporary file with the content of the URL.

        Raises:
            requests.RequestException: Base exception of ``requests``, see its
                docs for more detailed ones.

        Example:
            >>> import io, re, json
            >>> with url_as_file('https://api.github.com/meta', ext='json') as meta:
            ...     meta, json.load(io.open(meta, encoding='ascii'))['hooks']
            (u'/tmp/www-api.github.com-Ba5OhD.json', [u'192.30.252.0/22'])
    """
    if ext:
        ext = '.' + ext.strip('.')  # normalize extension
    url_hint = 'www-{}-'.format(urlparse(url).hostname or 'any')

    if url.startswith('file://'):
        url = os.path.abspath(url[len('file://'):])
    if os.path.isabs(url):
        with open(url, 'rb') as handle:
            content = handle.read()
    else:
        content = requests.get(url).content

    with tempfile.NamedTemporaryFile(suffix=ext or '', prefix=url_hint, delete=False) as handle:
        handle.write(content)

    try:
        yield handle.name
    finally:
        if os.path.exists(handle.name):
            os.remove(handle.name)