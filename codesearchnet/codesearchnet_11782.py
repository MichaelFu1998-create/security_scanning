def get_last_modified_timestamp(path, ignore=None):
    """
    Recursively finds the most recent timestamp in the given directory.
    """
    ignore = ignore or []
    if not isinstance(path, six.string_types):
        return
    ignore_str = ''
    if ignore:
        assert isinstance(ignore, (tuple, list))
        ignore_str = ' '.join("! -name '%s'" % _ for _ in ignore)
    cmd = 'find "'+path+'" ' + ignore_str + ' -type f -printf "%T@ %p\n" | sort -n | tail -1 | cut -f 1 -d " "'
         #'find '+path+' -type f -printf "%T@ %p\n" | sort -n | tail -1 | cut -d " " -f1
    ret = subprocess.check_output(cmd, shell=True)
    # Note, we round now to avoid rounding errors later on where some formatters
    # use different decimal contexts.
    try:
        ret = round(float(ret), 2)
    except ValueError:
        return
    return ret