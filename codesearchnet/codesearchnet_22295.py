def __read(path):
        '''
        Reads a File with contents in correct JSON format.
        Returns the data as Python objects.
        path - (string) path to the file
        '''
        try:
            with open(path, 'r') as data_file:
                data = data_file.read()
                data = json.loads(data)
                return data
        except IOError as err:
            pass
        except Exception as err:
            # Invalid JSON formatted files
            pass