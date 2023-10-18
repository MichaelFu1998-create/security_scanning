def map(self, map_function):
    """Return a new Streamlet by applying map_function to each element of this Streamlet.
    """
    from heronpy.streamlet.impl.mapbolt import MapStreamlet
    map_streamlet = MapStreamlet(map_function, self)
    self._add_child(map_streamlet)
    return map_streamlet