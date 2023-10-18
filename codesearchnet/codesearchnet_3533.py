def rm(self, key):
        """
        Remove file identified by `key`.

        :param str key: The file to delete
        """
        path = os.path.join(self.uri, key)
        os.remove(path)