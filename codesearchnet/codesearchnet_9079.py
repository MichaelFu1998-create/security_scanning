def all_folders(
        path_name, keyword='', has_date=False, date_fmt=DATE_FMT
) -> list:
    """
    Search all folders with criteria
    Returned list will be sorted by last modified

    Args:
        path_name: full path name
        keyword: keyword to search
        has_date: whether has date in file name (default False)
        date_fmt: date format to check for has_date parameter

    Returns:
        list: all folder names fulfilled criteria
    """
    if not os.path.exists(path=path_name): return []
    path_name = path_name.replace('\\', '/')

    if keyword:
        folders = sort_by_modified([
            f.replace('\\', '/') for f in glob.iglob(f'{path_name}/*{keyword}*')
            if os.path.isdir(f) and (f.replace('\\', '/').split('/')[-1][0] != '~')
        ])

    else:
        folders = sort_by_modified([
            f'{path_name}/{f}' for f in os.listdir(path=path_name)
            if os.path.isdir(f'{path_name}/{f}') and (f[0] != '~')
        ])

    if has_date:
        folders = filter_by_dates(folders, date_fmt=date_fmt)

    return folders