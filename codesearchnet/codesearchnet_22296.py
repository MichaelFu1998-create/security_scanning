def __write(path, data, mode="w"):
        '''
        Writes to a File. Returns the data written.
        path - (string) path to the file to write to.
        data - (json) data from a request.
        mode - (string) mode to open the file in. Default to 'w'. Overwrites.
        '''
        with open(path, mode) as data_file:
            data = json.dumps(data, indent=4)
            data_file.write(data)
            return data