def remove_repository(self, path=None, removeEmptyDirs=True):
        """
        Remove all repository from path along with all repository tracked files.

        :Parameters:
            #. path (None, string): The path the repository to remove.
            #. removeEmptyDirs (boolean): Whether to remove remaining empty
               directories.
        """
        assert isinstance(removeEmptyDirs, bool), "removeEmptyDirs must be boolean"
        if path is not None:
            if path != self.__path:
                repo = Repository()
                repo.load_repository(path)
            else:
                repo = self
        else:
            repo = self
        assert repo.path is not None, "path is not given and repository is not initialized"
        # remove repo files and directories
        for fdict in reversed(repo.get_repository_state()):
            relaPath   = list(fdict)[0]
            realPath   = os.path.join(repo.path, relaPath)
            path, name = os.path.split(realPath)
            if fdict[relaPath]['type'] == 'file':
                if os.path.isfile(realPath):
                    os.remove(realPath)
                if os.path.isfile(os.path.join(repo.path,path,self.__fileInfo%name)):
                    os.remove(os.path.join(repo.path,path,self.__fileInfo%name))
                if os.path.isfile(os.path.join(repo.path,path,self.__fileLock%name)):
                    os.remove(os.path.join(repo.path,path,self.__fileLock%name))
                if os.path.isfile(os.path.join(repo.path,path,self.__fileClass%name)):
                    os.remove(os.path.join(repo.path,path,self.__fileClass%name))
            elif fdict[relaPath]['type'] == 'dir':
                if os.path.isfile(os.path.join(realPath,self.__dirInfo)):
                    os.remove(os.path.join(realPath,self.__dirInfo))
                if os.path.isfile(os.path.join(realPath,self.__dirLock)):
                    os.remove(os.path.join(realPath,self.__dirLock))
                if not len(os.listdir(realPath)) and removeEmptyDirs:
                    shutil.rmtree( realPath )
        # remove repo information file
        if os.path.isfile(os.path.join(repo.path,self.__repoFile)):
            os.remove(os.path.join(repo.path,self.__repoFile))
        if os.path.isfile(os.path.join(repo.path,self.__repoLock)):
            os.remove(os.path.join(repo.path,self.__repoLock))