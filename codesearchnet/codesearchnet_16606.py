def _initfile(path, data="dict"):
    """Initialize an empty JSON file."""
    data = {} if data.lower() == "dict" else []
    # The file will need to be created if it doesn't exist
    if not os.path.exists(path):  # The file doesn't exist
        # Raise exception if the directory that should contain the file doesn't
        # exist
        dirname = os.path.dirname(path)
        if dirname and not os.path.exists(dirname):
            raise IOError(
                ("Could not initialize empty JSON file in non-existant "
                 "directory '{}'").format(os.path.dirname(path))
            )
        # Write an empty file there
        with open(path, "w") as f:
            json.dump(data, f)
        return True
    elif os.path.getsize(path) == 0:  # The file is empty
        with open(path, "w") as f:
            json.dump(data, f)
    else:  # The file exists and contains content
        return False