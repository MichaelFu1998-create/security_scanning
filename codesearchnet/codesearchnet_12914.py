def concatclusts(outhandle, alignbits):
    """ concatenates sorted aligned cluster tmpfiles and removes them."""
    with gzip.open(outhandle, 'wb') as out:
        for fname in alignbits:
            with open(fname) as infile:
                out.write(infile.read()+"//\n//\n")