def add_directory(self, relativePath, info=None):
        """
        Adds a directory in the repository and creates its
        attribute in the Repository with utc timestamp.
        It insures adding all the missing directories in the path.

        :Parameters:
            #. relativePath (string): The relative to the repository path of the directory to add in the repository.
            #. info (None, string, pickable object): Any random info about the folder.

        :Returns:
            #. info (dict): The directory info dict.
        """
        path = os.path.normpath(relativePath)
        # create directories
        currentDir  = self.path
        currentDict = self
        if path in ("","."):
            return currentDict
        save = False
        for dir in path.split(os.sep):
            dirPath = os.path.join(currentDir, dir)
            # create directory
            if not os.path.exists(dirPath):
                 os.mkdir(dirPath)
            # create dictionary key
            currentDict = dict.__getitem__(currentDict, "directories")
            if currentDict.get(dir, None) is None:
                save = True
                currentDict[dir] = {"directories":{}, "files":{},
                                    "timestamp":datetime.utcnow(),
                                    "id":str(uuid.uuid1()),
                                    "info": info} # INFO MUST BE SET ONLY FOR THE LAST DIRECTORY

            currentDict = currentDict[dir]
            currentDir  = dirPath
        # save repository
        if save:
            self.save()
        # return currentDict
        return currentDict