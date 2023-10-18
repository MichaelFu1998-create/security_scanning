def reduce_by_key_and_window(self, window_config, reduce_function):
    """Return a new Streamlet in which each (key, value) pair of this Streamlet are collected
       over the time_window and then reduced using the reduce_function
    """
    from heronpy.streamlet.impl.reducebykeyandwindowbolt import ReduceByKeyAndWindowStreamlet
    reduce_streamlet = ReduceByKeyAndWindowStreamlet(window_config, reduce_function, self)
    self._add_child(reduce_streamlet)
    return reduce_streamlet