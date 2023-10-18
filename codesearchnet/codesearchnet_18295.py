def get_file_info_by_id(self, id):
        """
        Given an id, get the corresponding file info as the following:\n
        (relative path joined with file name, file info dict)

        Parameters:
            #. id (string): The file unique id string.

        :Returns:
            #. relativePath (string): The file relative path joined with file name.
               If None, it means file was not found.
            #. info (None, dictionary): The file information dictionary.
               If None, it means file was not found.
        """
        for path, info in self.walk_files_info():
            if info['id']==id:
                return path, info
        # none was found
        return None, None