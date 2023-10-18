def is_compressed_json_file(abspath):
    """Test a file is a valid json file.

    - *.json: uncompressed, utf-8 encode json file
    - *.js: uncompressed, utf-8 encode json file
    - *.gz: compressed, utf-8 encode json file
    """
    abspath = abspath.lower()
    fname, ext = os.path.splitext(abspath)
    if ext in [".json", ".js"]:
        is_compressed = False
    elif ext == ".gz":
        is_compressed = True
    else:
        raise ValueError(
            "'%s' is not a valid json file. "
            "extension has to be '.json' or '.js' for uncompressed, '.gz' "
            "for compressed." % abspath)
    return is_compressed