def mkdir(self, folder):
        """ Creates a folder in the server

        :param folder: the folder to be created.
        :type folder: string
        """
        current_folder = self._ftp.pwd()
        #creates the necessary folders on
        #the server if they don't exist
        folders = folder.split('/')
        for fld in folders:
            try:
                self.cd(fld)
            except error_perm:  # folder does not exist
                self._ftp.mkd(fld)
                self.cd(fld)
        self.cd(current_folder)