def decode(in_file, out_file=None, mode=None, quiet=0):
    """Decode uuencoded file"""
    #
    # Open the input file, if needed.
    #
    opened_files = []
    if in_file == '-':
        in_file = sys.stdin
    elif isinstance(in_file, basestring):
        in_file = open(in_file)
        opened_files.append(in_file)
    try:
        #
        # Read until a begin is encountered or we've exhausted the file
        #
        while True:
            hdr = in_file.readline()
            if not hdr:
                raise Error('No valid begin line found in input file')
            if not hdr.startswith('begin'):
                continue
            hdrfields = hdr.split(' ', 2)
            if len(hdrfields) == 3 and hdrfields[0] == 'begin':
                try:
                    int(hdrfields[1], 8)
                    break
                except ValueError:
                    pass
        if out_file is None:
            out_file = hdrfields[2].rstrip()
            if os.path.exists(out_file):
                raise Error('Cannot overwrite existing file: %s' % out_file)
        if mode is None:
            mode = int(hdrfields[1], 8)
        #
        # Open the output file
        #
        if out_file == '-':
            out_file = sys.stdout
        elif isinstance(out_file, basestring):
            fp = open(out_file, 'wb')
            try:
                os.path.chmod(out_file, mode)
            except AttributeError:
                pass
            out_file = fp
            opened_files.append(out_file)
        #
        # Main decoding loop
        #
        s = in_file.readline()
        while s and s.strip() != 'end':
            try:
                data = binascii.a2b_uu(s)
            except binascii.Error, v:
                # Workaround for broken uuencoders by /Fredrik Lundh
                nbytes = (((ord(s[0])-32) & 63) * 4 + 5) // 3
                data = binascii.a2b_uu(s[:nbytes])
                if not quiet:
                    sys.stderr.write("Warning: %s\n" % v)
            out_file.write(data)
            s = in_file.readline()
        if not s:
            raise Error('Truncated input file')
    finally:
        for f in opened_files:
            f.close()