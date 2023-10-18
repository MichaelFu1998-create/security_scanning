def _barnes(self, pos):
        """Creates a barnes interpolant & calculates its values"""
        b_in = self.b_in
        dist = lambda x: np.sqrt(np.dot(x,x))
        #we take a filter size as the max distance between the grids along
        #x or y:
        sz = self.npts[1]
        coeffs = self.get_values(self.barnes_params)

        b = BarnesInterpolationND(
            b_in, coeffs, filter_size=self.filtsize, damp=0.9, iterations=3,
            clip=self.local_updates, clipsize=self.barnes_clip_size,
            blocksize=100  # FIXME magic blocksize
        )
        return b(pos)