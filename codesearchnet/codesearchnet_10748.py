def to_json(data, filename='data.json', indent=4):
    """
    Write an object to a json file

    :param data: The object
    :param filename: The name of the file
    :param indent: The indentation of the file
    :return: None
    """

    with open(filename, 'w') as f:
        f.write(json.dumps(data, indent=indent))