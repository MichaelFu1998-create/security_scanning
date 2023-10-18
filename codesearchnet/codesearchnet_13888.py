def age(self, id):

        """ Returns the age of the cache entry, in days.
        """

        path = self.hash(id)
        if os.path.exists(path):
            modified = datetime.datetime.fromtimestamp(os.stat(path)[8])
            age = datetime.datetime.today() - modified
            return age.days
        else:
            return 0