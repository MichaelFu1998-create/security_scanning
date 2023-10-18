def hashsum(filename):
    """Return a hash of the file From <http://stackoverflow.com/a/7829658>"""

    with open(filename, mode='rb') as f:
        d = hashlib.sha1()
        for buf in iter(partial(f.read, 2**20), b''):
            d.update(buf)
    return d.hexdigest()