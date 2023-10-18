def save_file(filename, source, folder="Downloads"):
    """
    Download and save a file at path

    :param filename: The name of the file
    :param source: The location of the resource online
    :param folder: The directory the file will be saved in
    :return: None
    """

    r = requests.get(source, stream=True)
    if r.status_code == 200:
        if not path.isdir(folder):
            makedirs(folder, exist_ok=True)
        with open("%s/%s" % (folder, filename), 'wb') as f:
            for chunk in r:
                f.write(chunk)