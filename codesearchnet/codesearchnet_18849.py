def rm(self, filename):
        """ Delete a file from the server.

        :param filename: the file to be deleted.
        :type filename: string
        """
        try:
            self._ftp.delete(filename)
        except error_perm:  # target is either a directory
                            # either it does not exist
            try:
                current_folder = self._ftp.pwd()
                self.cd(filename)
            except error_perm:
                print('550 Delete operation failed %s '
                      'does not exist!' % (filename,))
            else:
                self.cd(current_folder)
                print('550 Delete operation failed %s '
                      'is a folder. Use rmdir function '
                      'to delete it.' % (filename,))