def load_file_as_yaml(path):
    """
    Given a filepath, loads the file as a dictionary from YAML

    :param path: The path to a YAML file
    """
    with open(path, "r") as f:
      raw_yaml = f.read()
      parsed_dict = yaml.load(raw_yaml)
    return parsed_dict