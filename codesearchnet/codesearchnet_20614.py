def get(self, key):
        """
        Retrieve pandas object or group of Numpy ndarrays
        stored in file

        Parameters
        ----------
        key : object

        Returns
        -------
        obj : type of object stored in file
        """
        node = self.get_node(key)
        if node is None:
            raise KeyError('No object named %s in the file' % key)

        if hasattr(node, 'attrs'):
            if 'pandas_type' in node.attrs:
                return self._read_group(node)

        return self._read_array(node)