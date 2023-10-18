def clear_cache(module_name: str, keep_database: bool = True) -> None:
    """Clear all downloaded files."""
    data_dir = get_data_dir(module_name)
    if not os.path.exists(data_dir):
        return
    for name in os.listdir(data_dir):
        if name in {'config.ini', 'cfg.ini'}:
            continue
        if name == 'cache.db' and keep_database:
            continue
        path = os.path.join(data_dir, name)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

        os.rmdir(data_dir)