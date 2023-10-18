def download_folder(self, folder='', target_folder=''):
        """ Downloads a whole folder from the server.
        FtpHandler.download_folder() will download all the files
        from the server in the working directory.

        :param folder: the absolute path for the folder on the server.

        :type folder: string
        :param target_folder: absolute or relative path for the
                              destination folder default is the
                              working directory.
        :type target_folder: string
        """
        files, folders = self.ls(folder)
        for fl in files:
            self.download(join(folder, fl), target_folder)
        for fld in folders:
            self.download_folder(join(folder, fld), target_folder)