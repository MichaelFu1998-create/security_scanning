def filter_by_dates(files_or_folders: list, date_fmt=DATE_FMT) -> list:
    """
    Filter files or dates by date patterns

    Args:
        files_or_folders: list of files or folders
        date_fmt: date format

    Returns:
        list
    """
    r = re.compile(f'.*{date_fmt}.*')
    return list(filter(
        lambda vv: r.match(vv.replace('\\', '/').split('/')[-1]) is not None,
        files_or_folders,
    ))