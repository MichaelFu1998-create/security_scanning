def yaml_get_data(filename):
    """Get data from .yml file
    """
    with open(filename, 'rb') as fd:
        yaml_data = yaml.load(fd)
        return yaml_data
    return False