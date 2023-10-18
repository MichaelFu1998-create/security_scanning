def download(self, source_file, target_folder=''):
        """ Downloads a file from the FTP server to target folder

        :param source_file: the absolute path for the file on the server
                   it can be the one of the files coming from
                   FtpHandler.dir().
        :type source_file: string
        :param target_folder: relative or absolute path of the
                              destination folder default is the
                              working directory.
        :type target_folder: string
        """
        current_folder = self._ftp.pwd()

        if not target_folder.startswith('/'):  # relative path
            target_folder = join(getcwd(), target_folder)

        folder = os.path.dirname(source_file)
        self.cd(folder)

        if folder.startswith("/"):
            folder = folder[1:]

        destination_folder = join(target_folder, folder)
        if not os.path.exists(destination_folder):
            print("Creating folder", destination_folder)
            os.makedirs(destination_folder)

        source_file = os.path.basename(source_file)
        destination = join(destination_folder, source_file)
        try:
            with open(destination, 'wb') as result:
                self._ftp.retrbinary('RETR %s' % (source_file,),
                                     result.write)
        except error_perm as e:  # source_file is a folder
            print(e)
            remove(join(target_folder, source_file))
            raise
        self._ftp.cwd(current_folder)