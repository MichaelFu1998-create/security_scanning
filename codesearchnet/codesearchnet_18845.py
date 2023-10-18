def cd(self, folder):
        """ Changes the working directory on the server.

        :param folder: the desired directory.
        :type folder: string
        """
        if folder.startswith('/'):
            self._ftp.cwd(folder)
        else:
            for subfolder in folder.split('/'):
                if subfolder:
                    self._ftp.cwd(subfolder)