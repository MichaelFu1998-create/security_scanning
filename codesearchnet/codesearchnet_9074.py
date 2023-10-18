def _load_yaml_(file_name):
    """
    Load assets infomation from file

    Args:
        file_name: file name

    Returns:
        dict
    """
    if not os.path.exists(file_name): return dict()

    with open(file_name, 'r', encoding='utf-8') as fp:
        return YAML().load(stream=fp)