def _get_stream(filename, openfunction=open, mode='r'):
    """Return open stream if *filename* can be opened with *openfunction* or else ``None``."""
    try:
        stream = openfunction(filename, mode=mode)
    except (IOError, OSError) as err:
        # An exception might be raised due to two reasons, first the openfunction is unable to open the file, in this
        # case we have to ignore the error and return None. Second is when openfunction can't open the file because
        # either the file isn't there or the permissions don't allow access.
        if errno.errorcode[err.errno] in ['ENOENT', 'EACCES']:
            six.reraise(*sys.exc_info())
        return None
    if mode.startswith('r'):
        # additional check for reading (eg can we uncompress) --- is this needed?
        try:
            stream.readline()
        except IOError:
            stream.close()
            stream = None
        except:
            stream.close()
            raise
        else:
            stream.close()
            stream = openfunction(filename, mode=mode)
    return stream