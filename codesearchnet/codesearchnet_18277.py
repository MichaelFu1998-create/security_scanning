def get_list_representation(self):
        """
        Gets a representation of the Repository content in a list of directories(files) format.

        :Returns:
            #. repr (list): The list representation of the Repository content.
        """
        if self.__path is None:
            return []
        repr = [ self.__path+":["+','.join(list(dict.__getitem__(self, 'files')))+']' ]
        # walk directories
        for directory in sorted(list(self.walk_directories_relative_path())):
            directoryRepr = os.path.normpath(directory)
            # get directory info
            dirInfoDict, errorMessage = self.get_directory_info(directory)
            assert dirInfoDict is not None, errorMessage
            directoryRepr += ":["+','.join( list(dict.__getitem__(dirInfoDict, 'files')))+']'
            repr.append(directoryRepr)
        return repr