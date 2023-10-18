def all_files(
        path_name, keyword='', ext='', full_path=True,
        has_date=False, date_fmt=DATE_FMT
) -> list:
    """
    Search all files with criteria
    Returned list will be sorted by last modified

    Args:
        path_name: full path name
        keyword: keyword to search
        ext: file extensions, split by ','
        full_path: whether return full path (default True)
        has_date: whether has date in file name (default False)
        date_fmt: date format to check for has_date parameter

    Returns:
        list: all file names with criteria fulfilled
    """
    if not os.path.exists(path=path_name): return []
    path_name = path_name.replace('\\', '/')

    if keyword or ext:
        keyword = f'*{keyword}*' if keyword else '*'
        if not ext: ext = '*'
        files = sort_by_modified([
            f.replace('\\', '/') for f in glob.iglob(f'{path_name}/{keyword}.{ext}')
            if os.path.isfile(f) and (f.replace('\\', '/').split('/')[-1][0] != '~')
        ])

    else:
        files = sort_by_modified([
            f'{path_name}/{f}' for f in os.listdir(path=path_name)
            if os.path.isfile(f'{path_name}/{f}') and (f[0] != '~')
        ])

    if has_date:
        files = filter_by_dates(files, date_fmt=date_fmt)

    return files if full_path else [f.split('/')[-1] for f in files]