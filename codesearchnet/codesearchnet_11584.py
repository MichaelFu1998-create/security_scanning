def _getTarball(url, into_directory, cache_key, origin_info=None):
    '''unpack the specified tarball url into the specified directory'''

    try:
        access_common.unpackFromCache(cache_key, into_directory)
    except KeyError as e:
        tok = settings.getProperty('github', 'authtoken')
        headers = {}
        if tok is not None:
            headers['Authorization'] = 'token ' + str(tok)

        logger.debug('GET %s', url)
        response = requests.get(url, allow_redirects=True, stream=True, headers=headers)
        response.raise_for_status()

        logger.debug('getting file: %s', url)
        logger.debug('headers: %s', response.headers)
        response.raise_for_status()

        # github doesn't exposes hashes of the archives being downloaded as far
        # as I can tell :(
        access_common.unpackTarballStream(
                    stream = response,
            into_directory = into_directory,
                      hash = {},
                 cache_key = cache_key,
               origin_info = origin_info
        )