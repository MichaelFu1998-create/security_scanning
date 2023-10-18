def _save(self):
        """
        Saves the color information in the cache as XML.
        """
        if not os.path.exists(self.cache):
            os.makedirs(self.cache)

        path = os.path.join(self.cache, self.name + ".xml")
        f = open(path, "w")
        f.write(self.xml)
        f.close()