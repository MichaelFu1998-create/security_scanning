def save(self, filename):
        """Pickle the whole collection to *filename*.
        
        If no extension is provided, ".collection" is appended.
        """
        cPickle.dump(self, open(self._canonicalize(filename), 'wb'), 
                     protocol=cPickle.HIGHEST_PROTOCOL)