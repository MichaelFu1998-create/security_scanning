def write_data(data, filename):
    """Call right func to save data according to file extension
    """
    name, ext = get_file_extension(filename)
    func = json_write_data if ext == '.json' else yaml_write_data
    return func(data, filename)