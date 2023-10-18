def CreateMD5(source_filename, target_filename=None):
    '''
    Creates a md5 file from a source file (contents are the md5 hash of source file)

    :param unicode source_filename:
        Path to source file

    :type target_filename: unicode or None
    :param target_filename:
        Name of the target file with the md5 contents

        If None, defaults to source_filename + '.md5'
    '''
    if target_filename is None:
        target_filename = source_filename + '.md5'

    from six.moves.urllib.parse import urlparse
    source_url = urlparse(source_filename)

    # Obtain MD5 hex
    if _UrlIsLocal(source_url):
        # If using a local file, we can give Md5Hex the filename
        md5_contents = Md5Hex(filename=source_filename)
    else:
        # Md5Hex can't handle remote files, we open it and pray we won't run out of memory.
        md5_contents = Md5Hex(contents=GetFileContents(source_filename, binary=True))

    # Write MD5 hash to a file
    CreateFile(target_filename, md5_contents)