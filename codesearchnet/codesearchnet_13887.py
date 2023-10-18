def hash(self, id):

        """ Creates a unique filename in the cache for the id.
        """

        h = md5(id).hexdigest()
        return os.path.join(self.path, h+self.type)