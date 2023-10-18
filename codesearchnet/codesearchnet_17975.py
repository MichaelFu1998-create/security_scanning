def oslicer(self, tile):
        """ Opposite slicer, the outer part wrt to a field """
        mask = None
        vecs = tile.coords(form='meshed')
        for v in vecs:
            v[self.slicer] = -1
            mask = mask & (v > 0) if mask is not None else (v>0)
        return tuple(np.array(i).astype('int') for i in zip(*[v[mask] for v in vecs]))