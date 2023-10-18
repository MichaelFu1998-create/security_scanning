def reduce_by_window(self, window_config, reduce_function):
    """Return a new Streamlet in which each element of this Streamlet are collected
      over a window defined by window_config and then reduced using the reduce_function
      reduce_function takes two element at one time and reduces them to one element that
      is used in the subsequent operations.
    """
    from heronpy.streamlet.impl.reducebywindowbolt import ReduceByWindowStreamlet
    reduce_streamlet = ReduceByWindowStreamlet(window_config, reduce_function, self)
    self._add_child(reduce_streamlet)
    return reduce_streamlet