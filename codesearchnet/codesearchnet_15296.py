def get_data_dir(module_name: str) -> str:
    """Ensure the appropriate Bio2BEL data directory exists for the given module, then returns the file path.

    :param module_name: The name of the module. Ex: 'chembl'
    :return: The module's data directory
    """
    module_name = module_name.lower()
    data_dir = os.path.join(BIO2BEL_DIR, module_name)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir