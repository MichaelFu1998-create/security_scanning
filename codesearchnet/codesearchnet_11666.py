def _downloadToCache(stream, hashinfo={}, origin_info=dict()):
    ''' Download the specified stream to a temporary cache directory, and
        returns a cache key that can be used to access/remove the file.
        You should use either removeFromCache(cache_key) or _moveCachedFile to
        move the downloaded file to a known key after downloading.
    '''
    hash_name  = None
    hash_value = None
    m = None

    if len(hashinfo):
        # check for hashes in preferred order. Currently this is just sha256
        # (which the registry uses). Initial investigations suggest that github
        # doesn't return a header with the hash of the file being downloaded.
        for h in ('sha256',):
            if h in hashinfo:
                hash_name  = h
                hash_value = hashinfo[h]
                m = getattr(hashlib, h)()
                break
        if not hash_name:
            logger.warning('could not find supported hash type in %s', hashinfo)

    cache_dir = folders.cacheDirectory()
    fsutils.mkDirP(cache_dir)
    file_size = 0

    (download_file, download_fname) = tempfile.mkstemp(dir=cache_dir, suffix='.locked')

    with os.fdopen(download_file, 'wb') as f:
        f.seek(0)
        for chunk in stream.iter_content(4096):
            f.write(chunk)
            if hash_name:
                m.update(chunk)

        if hash_name:
            calculated_hash = m.hexdigest()
            logger.debug(
                'calculated %s hash: %s check against: %s' % (
                    hash_name, calculated_hash, hash_value
                )
            )
            if hash_value and (hash_value != calculated_hash):
                raise Exception('Hash verification failed.')
        file_size = f.tell()
        logger.debug('wrote tarfile of size: %s to %s', file_size, download_fname)
        f.truncate()

    extended_origin_info = {
        'hash': hashinfo,
        'size': file_size
    }
    extended_origin_info.update(origin_info)
    ordered_json.dump(download_fname + '.json', extended_origin_info)
    return os.path.basename(download_fname)