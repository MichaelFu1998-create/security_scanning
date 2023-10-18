def transform(self, transform_operator):
    """Returns a  new Streamlet by applying the transform_operator on each element of this
    streamlet. The transform_function is of the type TransformOperator.
    Before starting to cycle over the Streamlet, the open function of the transform_operator is
    called. This allows the transform_operator to do any kind of initialization/loading, etc.
    """
    from heronpy.streamlet.impl.transformbolt import TransformStreamlet
    transform_streamlet = TransformStreamlet(transform_operator, self)
    self._add_child(transform_streamlet)
    return transform_streamlet