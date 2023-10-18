def generate_dirlist_html(FS, filepath):
    """
    Generate directory listing HTML

    Arguments:
        FS (FS): filesystem object to read files from
        filepath (str): path to generate directory listings for

    Keyword Arguments:
        list_dir (callable: list[str]): list file names in a directory
        isdir (callable: bool): os.path.isdir

    Yields:
        str: lines of an HTML table
    """
    yield '<table class="dirlist">'
    if filepath == '/':
        filepath = ''
    for name in FS.listdir(filepath):
        full_path = pathjoin(filepath, name)
        if FS.isdir(full_path):
            full_path = full_path + '/'
        yield u'<tr><td><a href="{0}">{0}</a></td></tr>'.format(
            cgi.escape(full_path))  # TODO XXX
    yield '</table>'