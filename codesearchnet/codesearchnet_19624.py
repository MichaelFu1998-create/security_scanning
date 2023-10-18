def flows(args):
    """
    todo : add some example
    :param args:
    :return:
    """

    def flow_if_not(fun):
        # t = type(fun)
        if isinstance(fun, iterator):
            return fun
        elif isinstance(fun, type) and 'itertools' in str(fun.__class__):
            return fun
        else:
            try:
                return flow(fun)
            except AttributeError:
                # generator object has no attribute '__module__'
                return fun

    return FlowList(map(flow_if_not, args))