def _base64_to_file(b64str, outfpath, writetostrio=False):
    '''This converts the base64 encoded string to a file.

    Parameters
    ----------

    b64str : str
        A base64 encoded strin that is the output of `base64.b64encode`.

    outfpath : str
        The path to where the file will be written. This should include an
        appropriate extension for the file (e.g. a base64 encoded string that
        represents a PNG should have its `outfpath` end in a '.png') so the OS
        can open these files correctly.

    writetostrio : bool
        If this is True, will return a StringIO object with the binary stream
        decoded from the base64-encoded input string `b64str`. This can be
        useful to embed these into other files without having to write them to
        disk.

    Returns
    -------

    str or StringIO object
        If `writetostrio` is False, will return the output file's path as a
        str. If it is True, will return a StringIO object directly. If writing
        the file fails in either case, will return None.

    '''

    try:

        filebytes = base64.b64decode(b64str)

        # if we're writing back to a stringio object
        if writetostrio:

            outobj = StrIO(filebytes)
            return outobj

        # otherwise, we're writing to an actual file
        else:

            with open(outfpath,'wb') as outfd:
                outfd.write(filebytes)

            if os.path.exists(outfpath):
                return outfpath
            else:
                LOGERROR('could not write output file: %s' % outfpath)
                return None

    except Exception as e:

        LOGEXCEPTION('failed while trying to convert '
                     'b64 string to file %s' % outfpath)
        return None