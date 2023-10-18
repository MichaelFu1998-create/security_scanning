def update_missing(**kwargs):
    """
    Update number of trials for missing values
    """
    data_path = os.environ.get(BBG_ROOT, '').replace('\\', '/')
    if not data_path: return
    if len(kwargs) == 0: return

    log_path = f'{data_path}/Logs/{missing_info(**kwargs)}'

    cnt = len(files.all_files(log_path)) + 1
    files.create_folder(log_path)
    open(f'{log_path}/{cnt}.log', 'a').close()