def get_file_relative_path_by_id(self, id):
        """
        Given an id, get the corresponding file info relative path joined with file name.

        Parameters:
            #. id (string): The file unique id string.

        :Returns:
            #. relativePath (string): The file relative path joined with file name.
               If None, it means file was not found.
        """
        for path, info in self.walk_files_info():
            if info['id']==id:
                return path
        # none was found
        return None