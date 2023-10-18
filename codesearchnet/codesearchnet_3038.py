def outer_join(self, join_streamlet, window_config, join_function):
    """Return a new Streamlet by outer join_streamlet with this streamlet
    """
    from heronpy.streamlet.impl.joinbolt import JoinStreamlet, JoinBolt

    join_streamlet_result = JoinStreamlet(JoinBolt.OUTER, window_config,
                                          join_function, self, join_streamlet)
    self._add_child(join_streamlet_result)
    join_streamlet._add_child(join_streamlet_result)
    return join_streamlet_result