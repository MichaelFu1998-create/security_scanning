def unpack_apply_message(bufs, g=None, copy=True):
    """Unpack f,args,kwargs from buffers packed by pack_apply_message().

    Returns: original f,args,kwargs
    """
    bufs = list(bufs)  # allow us to pop
    assert len(bufs) >= 2, "not enough buffers!"
    pf = buffer_to_bytes_py2(bufs.pop(0))
    f = uncan(pickle.loads(pf), g)
    pinfo = buffer_to_bytes_py2(bufs.pop(0))
    info = pickle.loads(pinfo)
    arg_bufs, kwarg_bufs = bufs[:info['narg_bufs']], bufs[info['narg_bufs']:]

    args = []
    for i in range(info['nargs']):
        arg, arg_bufs = deserialize_object(arg_bufs, g)
        args.append(arg)
    args = tuple(args)
    assert not arg_bufs, "Shouldn't be any arg bufs left over"

    kwargs = {}
    for key in info['kw_keys']:
        kwarg, kwarg_bufs = deserialize_object(kwarg_bufs, g)
        kwargs[key] = kwarg
    assert not kwarg_bufs, "Shouldn't be any kwarg bufs left over"

    return f, args, kwargs