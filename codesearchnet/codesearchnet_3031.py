def union(self, other_streamlet):
    """Returns a new Streamlet that consists of elements of both this and other_streamlet
    """
    from heronpy.streamlet.impl.unionbolt import UnionStreamlet
    union_streamlet = UnionStreamlet(self, other_streamlet)
    self._add_child(union_streamlet)
    other_streamlet._add_child(union_streamlet)
    return union_streamlet