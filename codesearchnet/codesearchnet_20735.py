def get_noneid_references(self):
        """
        Returns
        -------
        ndarray
        Array of references in self.reflst whose self id is None.
        """
        #return [self.reflst[idx] for idx, idval in enumerate(self) if idval is None]
        try:
            nun = np.array(None).astype(self.dtype)
            return np.array(self.reflst)[self == nun]
        except:
            nun = None
            return np.array(self.reflst)[self is None]