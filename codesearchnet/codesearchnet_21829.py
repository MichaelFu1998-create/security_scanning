def _broadcast_shape(*args):
    """Return the shape that would result from broadcasting the inputs"""
    #TODO: currently incorrect result if a Sequence is provided as an input
    shapes = [a.shape if hasattr(type(a), '__array_interface__')
              else () for a in args]
    ndim = max(len(sh) for sh in shapes) # new common ndim after broadcasting
    for i, sh in enumerate(shapes):
        if len(sh) < ndim:
            shapes[i] = (1,)*(ndim - len(sh)) + sh
    return tuple(max(sh[ax] for sh in shapes) for ax in range(ndim))