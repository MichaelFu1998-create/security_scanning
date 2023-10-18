def get_directory():
    """Get LanguageTool directory."""
    try:
        language_check_dir = cache['language_check_dir']
    except KeyError:
        def version_key(string):
            return [int(e) if e.isdigit() else e
                    for e in re.split(r"(\d+)", string)]

        def get_lt_dir(base_dir):
            paths = [
                path for path in
                glob.glob(os.path.join(base_dir, 'LanguageTool*'))
                if os.path.isdir(path)
            ]
            return max(paths, key=version_key) if paths else None

        base_dir = os.path.dirname(sys.argv[0])
        language_check_dir = get_lt_dir(base_dir)
        if not language_check_dir:
            try:
                base_dir = os.path.dirname(os.path.abspath(__file__))
            except NameError:
                pass
            else:
                language_check_dir = get_lt_dir(base_dir)
            if not language_check_dir:
                raise PathError("can't find LanguageTool directory in {!r}"
                                .format(base_dir))
        cache['language_check_dir'] = language_check_dir
    return language_check_dir