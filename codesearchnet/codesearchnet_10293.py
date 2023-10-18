def glob_parts(prefix, ext):
    """Find files from a continuation run"""
    if ext.startswith('.'):
        ext = ext[1:]
    files = glob.glob(prefix+'.'+ext) + glob.glob(prefix+'.part[0-9][0-9][0-9][0-9].'+ext)
    files.sort()   # at least some rough sorting...
    return files