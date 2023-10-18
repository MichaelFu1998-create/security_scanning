def pip_install(*args):
    """Send the given arguments to `pip install`.
    """
    download_cache = ('--download-cache=%s ' % options.paved.pip.download_cache) if options.paved.pip.download_cache else ''
    shv('pip install %s%s' % (download_cache, ' '.join(args)))