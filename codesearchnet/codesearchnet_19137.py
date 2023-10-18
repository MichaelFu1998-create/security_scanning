def copy(self, stack=False, copy_meta=False, memo=None):
        '''
        Copies the Feature object. Makes a copy of the features array.

        Parameters
        ----------
        stack : boolean, optional, default False
            Whether to stack the copy if this one is unstacked.

        copy_meta : boolean, optional, default False
            Also copy the metadata. If False, metadata in both points to the
            same object.
        '''
        if self.stacked:
            fs = deepcopy(self.stacked_features, memo)
            n_pts = self.n_pts.copy()
        elif stack:
            fs = np.vstack(self.features)
            n_pts = self.n_pts.copy()
        else:
            fs = deepcopy(self.features, memo)
            n_pts = None

        meta = deepcopy(self.meta, memo) if copy_meta else self.meta
        return Features(fs, n_pts, copy=False, **meta)