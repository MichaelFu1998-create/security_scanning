def _bufcountlines(filename, gzipped):
    """
    fast line counter. Used to quickly sum number of input reads when running
    link_fastqs to append files. """
    if gzipped:
        fin = gzip.open(filename)
    else:
        fin = open(filename)
    nlines = 0
    buf_size = 1024 * 1024
    read_f = fin.read # loop optimization
    buf = read_f(buf_size)
    while buf:
        nlines += buf.count('\n')
        buf = read_f(buf_size)
    fin.close()
    return nlines