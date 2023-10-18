def contents_of(f, encoding='utf-8'):
    """Helper to read the contents of the given file or path into a string with the given encoding.
    Encoding defaults to 'utf-8', other useful encodings are 'ascii' and 'latin-1'."""

    try:
        contents = f.read()
    except AttributeError:
        try:
            with open(f, 'r') as fp:
                contents = fp.read()
        except TypeError:
            raise ValueError('val must be file or path, but was type <%s>' % type(f).__name__)
        except OSError:
            if not isinstance(f, str_types):
                raise ValueError('val must be file or path, but was type <%s>' % type(f).__name__)
            raise

    if sys.version_info[0] == 3 and type(contents) is bytes:
        # in PY3 force decoding of bytes to target encoding
        return contents.decode(encoding, 'replace')
    elif sys.version_info[0] == 2 and encoding == 'ascii':
        # in PY2 force encoding back to ascii
        return contents.encode('ascii', 'replace')
    else:
        # in all other cases, try to decode to target encoding
        try:
            return contents.decode(encoding, 'replace')
        except AttributeError:
            pass
    # if all else fails, just return the contents "as is"
    return contents