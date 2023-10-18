def get_file_relative_path_by_name(self, name, skip=0):
        """
        Get file relative path given the file name. If file name is redundant in different
        directories in the repository, this method ensures to return all or some of the
        files according to skip value.

        Parameters:
            #. name (string): The file name.
            #. skip (None, integer): As file names can be identical, skip determines
               the number of satisfying files name to skip before returning.\n
               If None is given, a list of all files relative path will be returned.

        :Returns:
            #. relativePath (string, list): The file relative path.
               If None, it means file was not found.\n
               If skip is None a list of all found files relative paths will be returned.
        """
        if skip is None:
            paths = []
        else:
            paths = None
        for path, info in self.walk_files_info():
            _, n = os.path.split(path)
            if n==name:
                if skip is None:
                    paths.append(path)
                elif skip>0:
                    skip -= 1
                else:
                    paths = path
                    break
        return paths