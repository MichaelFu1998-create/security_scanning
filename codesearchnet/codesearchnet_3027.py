def filter(self, filter_function):
    """Return a new Streamlet containing only the elements that satisfy filter_function
    """
    from heronpy.streamlet.impl.filterbolt import FilterStreamlet
    filter_streamlet = FilterStreamlet(filter_function, self)
    self._add_child(filter_streamlet)
    return filter_streamlet