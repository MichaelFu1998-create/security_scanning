def upload(self, filename, location=''):
        """ Uploads a file on the server to the desired location

        :param filename: the name of the file to be uploaded.
        :type filename: string
        :param location: the directory in which the file will
                         be stored.
        :type location: string
        """
        current_folder = self._ftp.pwd()
        self.mkdir(location)
        self.cd(location)
        fl = open(filename, 'rb')
        filename = filename.split('/')[-1]
        self._ftp.storbinary('STOR %s' % filename, fl)
        fl.close()
        self.cd(current_folder)