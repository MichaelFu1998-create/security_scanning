def rmdir(self, foldername):
        """ Delete a folder from the server.

        :param foldername: the folder to be deleted.
        :type foldername: string
        """
        current_folder = self._ftp.pwd()
        try:
            self.cd(foldername)
        except error_perm:
            print('550 Delete operation failed folder %s '
                  'does not exist!' % (foldername,))
        else:
            self.cd(current_folder)
            try:
                self._ftp.rmd(foldername)
            except error_perm:  # folder not empty
                self.cd(foldername)
                contents = self.ls()
                #delete the files
                map(self._ftp.delete, contents[0])
                #delete the subfolders
                map(self.rmdir, contents[1])
                self.cd(current_folder)
                self._ftp.rmd(foldername)