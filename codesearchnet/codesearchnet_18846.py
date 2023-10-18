def ls(self, folder=''):
        """ Lists the files and folders of a specific directory
        default is the current working directory.

        :param folder: the folder to be listed.
        :type folder: string

        :returns: a tuple with the list of files in the folder
                  and the list of subfolders in the folder.
        """
        current_folder = self._ftp.pwd()
        self.cd(folder)
        contents = []
        self._ftp.retrlines('LIST', lambda a: contents.append(a))
        files = filter(lambda a: a.split()[0].startswith('-'), contents)
        folders = filter(lambda a: a.split()[0].startswith('d'), contents)
        files = map(lambda a: ' '.join(a.split()[8:]), files)
        folders = map(lambda a: ' '.join(a.split()[8:]), folders)
        self._ftp.cwd(current_folder)
        return files, folders