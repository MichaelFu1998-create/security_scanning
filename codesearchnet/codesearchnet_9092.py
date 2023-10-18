def current_missing(**kwargs) -> int:
    """
    Check number of trials for missing values

    Returns:
        int: number of trials already tried
    """
    data_path = os.environ.get(BBG_ROOT, '').replace('\\', '/')
    if not data_path: return 0
    return len(files.all_files(f'{data_path}/Logs/{missing_info(**kwargs)}'))