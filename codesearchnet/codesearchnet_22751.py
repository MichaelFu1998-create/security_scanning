def Md5Hex(filename=None, contents=None):
    '''
    :param unicode filename:
        The file from which the md5 should be calculated. If the filename is given, the contents
        should NOT be given.

    :param unicode contents:
        The contents for which the md5 should be calculated. If the contents are given, the filename
        should NOT be given.

    :rtype: unicode
    :returns:
        Returns a string with the hex digest of the stream.
    '''
    import io
    import hashlib
    md5 = hashlib.md5()

    if filename:
        stream = io.open(filename, 'rb')
        try:
            while True:
                data = stream.read(md5.block_size * 128)
                if not data:
                    break
                md5.update(data)
        finally:
            stream.close()

    else:
        md5.update(contents)

    return six.text_type(md5.hexdigest())