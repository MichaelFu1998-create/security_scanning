def yaml_write_data(yaml_data, filename):
    """Write data into a .yml file
    """
    with open(filename, 'w') as fd:
        yaml.dump(yaml_data, fd, default_flow_style=False)
        return True

    return False