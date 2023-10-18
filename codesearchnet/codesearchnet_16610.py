def with_data(path, data):
        """Initialize a new file that starts out with some data. Pass data
        as a list, dict, or JSON string.
        """
        # De-jsonize data if necessary
        if isinstance(data, str):
            data = json.loads(data)

        # Make sure this is really a new file
        if os.path.exists(path):
            raise ValueError("File exists, not overwriting data. Set the "
                             "'data' attribute on a normally-initialized "
                             "'livejson.File' instance if you really "
                             "want to do this.")
        else:
            f = File(path)
            f.data = data
            return f