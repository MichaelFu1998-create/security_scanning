def get_sha(a_file, settings=None):
    """
    Returns sha1 hash of the file supplied as an argument
    """
    if settings:
        error = settings["error"]
    else:
        error = ERROR_FN
    try:
        BLOCKSIZE = 65536
        hasher = hashlib.sha1()
        with io.open(a_file, "rb") as fh:
            buf = fh.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = fh.read(BLOCKSIZE)
        the_hash = hasher.hexdigest()
    except IOError:
        errmes = "File '{}' could not be read! Exiting!".format(a_file)
        error(errmes)
        sys.exit(1)
    except:
        errmes = "Unspecified error returning sha1 hash. Exiting!"
        error(errmes)
        sys.exit(1)
    return the_hash