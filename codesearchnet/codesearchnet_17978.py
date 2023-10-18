def _format_vector(self, vecs, form='broadcast'):
        """
        Format a 3d vector field in certain ways, see `coords` for a description
        of each formatting method.
        """
        if form == 'meshed':
            return np.meshgrid(*vecs, indexing='ij')
        elif form == 'vector':
            vecs = np.meshgrid(*vecs, indexing='ij')
            return np.rollaxis(np.array(np.broadcast_arrays(*vecs)),0,self.dim+1)
        elif form == 'flat':
            return vecs
        else:
            return [v[self._coord_slicers[i]] for i,v in enumerate(vecs)]