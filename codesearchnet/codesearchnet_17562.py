def get_path_relative_to_module(module_file_path, relative_target_path):
    """
    Calculate a path relative to the specified module file.

    :param module_file_path: The file path to the module.
    """
    module_path = os.path.dirname(module_file_path)
    path = os.path.join(module_path, relative_target_path)
    path = os.path.abspath(path)
    return path