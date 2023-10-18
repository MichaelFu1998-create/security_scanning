def dir(self, folder='', prefix=''):
        """ Lists all the files on the folder given as parameter.
        FtpHandler.dir() lists all the files on the server.

        :para folder: the folder to be listed.
        :type folder: string

        :param prefix: it does not belong to the interface,
                       it is used to recursively list the subfolders.

        :returns: a list with all the files in the server.
        """
        files, folders = self.ls(folder)
        result = files
        inner = []
        for fld in folders:
            try:
                inner += self.dir(folder + '/' + fld, prefix + fld + '/')
            except:
                pass
        result += inner
        if prefix:
            result = map(lambda a: prefix + a, result)
        return result