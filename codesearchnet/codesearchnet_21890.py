def _process_args(args, kwargs, prefer_local=True, recurse=True):
    """Select local or remote execution and prepare arguments accordingly.
    Assumes any remote args have already been moved to a common engine.

    Local execution will be chosen if:
    - all args are ordinary objects or Remote instances on the local engine; or
    - the local cache of all remote args is current, and prefer_local is True.
    Otherwise, remote execution will be chosen. 

    For remote execution, replaces any remote arg with its Id.
    For local execution, replaces any remote arg with its locally cached object
    Any arguments or kwargs that are Sequences will be recursed one level deep.

    Args:
      args (list)
      kwargs (dict)
      prefer_local (bool, optional): Whether cached local results are prefered
        if available, instead of returning Remote objects. Default is True.
    """
    this_engine = distob.engine.eid
    local_args = []
    remote_args = []
    execloc = this_engine  # the chosen engine id for execution of the call
    for a in args:
        id = None
        if isinstance(a, Remote):
            id = a._ref.id
        elif isinstance(a, Ref):
            id = a.id
        elif isinstance(a, Id):
            id = a
        if id is not None:
            if id.engine is this_engine:
                local_args.append(distob.engine[id])
                remote_args.append(distob.engine[id])
            else:
                if (prefer_local and isinstance(a, Remote) and 
                        a._obcache_current):
                    local_args.append(a._obcache)
                    remote_args.append(id)
                else:
                    # will choose remote execution
                    if execloc is not this_engine and id.engine is not execloc:
                        raise DistobValueError(
                            'two remote arguments are from different engines')
                    else:
                        execloc = id.engine
                        local_args.append(None)
                        remote_args.append(id)
        elif (isinstance(a, collections.Sequence) and
                not isinstance(a, string_types) and recurse):
            eid, ls, _ = _process_args(a, {}, prefer_local, recurse=False)
            if eid is not this_engine:
                if execloc is not this_engine and eid is not execloc:
                    raise DistobValueError(
                            'two remote arguments are from different engines')
                execloc = eid
            local_args.append(ls)
            remote_args.append(ls)
        else:
            # argument is an ordinary object
            local_args.append(a)
            remote_args.append(a)
    local_kwargs = dict()
    remote_kwargs = dict()
    for k, a in kwargs.items():
        id = None
        if isinstance(a, Remote):
            id = a._ref.id
        elif isinstance(a, Ref):
            id = a.id
        elif isinstance(a, Id):
            id = a
        if id is not None:
            if id.engine is this_engine:
                local_kwargs[k] = distob.engine[id]
                remote_kwargs[k] = distob.engine[id]
            else:
                if (prefer_local and isinstance(a, Remote) and
                        a._obcache_current):
                    local_kwargs[k] = a._obcache
                    remote_kwargs[k] = id
                else:
                    # will choose remote execution
                    if execloc is not this_engine and id.engine is not execloc:
                        raise DistobValueError(
                            'two remote arguments are from different engines')
                    else:
                        execloc = id.engine
                        local_kwargs[k] = None
                        remote_kwargs[k] = id
        elif (isinstance(a, collections.Sequence) and
                not isinstance(a, string_types) and recurse):
            eid, ls, _ = _process_args(a, {}, prefer_local, recurse=False)
            if eid is not this_engine:
                if execloc is not this_engine and eid is not execloc:
                    raise DistobValueError(
                            'two remote arguments are from different engines')
                execloc = eid
            local_kwargs[k] = ls
            remote_kwargs[k] = ls
        else:
            # argument is an ordinary object 
            local_kwargs[k] = a
            remote_kwargs[k] = a
    if execloc is this_engine:
        return execloc, tuple(local_args), local_kwargs
    else:
        return execloc, tuple(remote_args), remote_kwargs