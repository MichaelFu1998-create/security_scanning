def get_data(filename):
    """Calls right function according to file extension
    """
    name, ext = get_file_extension(filename)
    func = json_get_data if ext == '.json' else yaml_get_data
    return func(filename)