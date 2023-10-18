def flat_map(self, flatmap_function):
    """Return a new Streamlet by applying map_function to each element of this Streamlet
       and flattening the result
    """
    from heronpy.streamlet.impl.flatmapbolt import FlatMapStreamlet
    fm_streamlet = FlatMapStreamlet(flatmap_function, self)
    self._add_child(fm_streamlet)
    return fm_streamlet