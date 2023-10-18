def _parse_specs(specs, Ks):
    '''
    Set up the different functions we need to call.

    Returns:
        - a dict mapping base estimator functions to _FuncInfo objects.
          If the function needs_alpha, then the alphas attribute is an array
          of alpha values and pos is a corresponding array of indices.
          Otherwise, alphas is None and pos is a list containing a single index.
          Indices are >= 0 if they correspond to something in a spec,
          and negative if they're just used for a meta estimator but not
          directly requested.
        - an OrderedDict mapping functions to _MetaFuncInfo objects.
          alphas and pos are like for _FuncInfo; deps is a list of indices
          which should be passed to the estimator. Note that these might be
          other meta functions; this list is guaranteed to be in an order
          such that all dependencies are resolved before calling that function.
          If no such order is possible, raise ValueError.
        - the number of meta-only results

    # TODO: update doctests for _parse_specs

    >>> _parse_specs(['renyi:.8', 'hellinger', 'renyi:.9'])
    ({<function alpha_div at 0x10954f848>:
            _FuncInfo(alphas=[0.8, 0.5, 0.9], pos=[-1, -2, -3])},
     OrderedDict([
        (<function hellinger at 0x10954fc80>,
            _MetaFuncInfo(alphas=None, pos=[1], deps=[array(-2)])),
        (<function renyi at 0x10954fcf8>,
            _MetaFuncInfo(alphas=[0.8, 0.9], pos=[0, 2], deps=[-1, -3]))
     ]), 3)

    >>> _parse_specs(['renyi:.8', 'hellinger', 'renyi:.9', 'l2'])
    ({<function alpha_div at 0x10954f848>:
        _FuncInfo(alphas=[0.8, 0.5, 0.9], pos=[-1, -2, -3]),
      <function linear at 0x10954f758>: _FuncInfo(alphas=None, pos=[-4])
     }, OrderedDict([
        (<function hellinger at 0x10954fc80>,
            _MetaFuncInfo(alphas=None, pos=[1], deps=[array(-2)])),
        (<function l2 at 0x10954fde8>,
            _MetaFuncInfo(alphas=None, pos=[3], deps=[-4])),
        (<function renyi at 0x10954fcf8>,
            _MetaFuncInfo(alphas=[0.8, 0.9], pos=[0, 2], deps=[-1, -3]))
     ]), 4)

    >>> _parse_specs(['renyi:.8', 'hellinger', 'renyi:.9', 'l2', 'linear'])
    ({<function alpha_div at 0x10954f848>:
        _FuncInfo(alphas=[0.8, 0.5, 0.9], pos=[-1, -2, -3]),
      <function linear at 0x10954f758>: _FuncInfo(alphas=None, pos=[4])
     }, OrderedDict([
        (<function hellinger at 0x10954fc80>,
            _MetaFuncInfo(alphas=None, pos=[1], deps=[array(-2)])),
        (<function l2 at 0x10954fde8>,
            _MetaFuncInfo(alphas=None, pos=[3], deps=[4])),
        (<function renyi at 0x10954fcf8>,
            _MetaFuncInfo(alphas=[0.8, 0.9], pos=[0, 2], deps=[-1, -3]))
     ]), 3)
    '''
    funcs = {}
    metas = {}
    meta_deps = defaultdict(set)

    def add_func(func, alpha=None, pos=None):
        needs_alpha = getattr(func, 'needs_alpha', False)
        is_meta = hasattr(func, 'needs_results')

        d = metas if is_meta else funcs
        if func not in d:
            if needs_alpha:
                args = {'alphas': [alpha], 'pos': [pos]}
            else:
                args = {'alphas': None, 'pos': [pos]}

            if not is_meta:
                d[func] = _FuncInfo(**args)
            else:
                d[func] = _MetaFuncInfo(deps=[], **args)
                for req in func.needs_results:
                    if callable(req.alpha):
                        req_alpha = req.alpha(alpha)
                    else:
                        req_alpha = req.alpha
                    add_func(req.func, alpha=req_alpha)
                    meta_deps[func].add(req.func)
                    meta_deps[req.func]  # make sure required func is in there

        else:
            # already have an entry for the func
            # need to give it this pos, if it's not None
            # and also make sure that the alpha is present
            info = d[func]
            if not needs_alpha:
                if pos is not None:
                    if info.pos != [None]:
                        msg = "{} passed more than once"
                        raise ValueError(msg.format(func_name))

                    info.pos[0] = pos
            else:  # needs alpha
                try:
                    idx = info.alphas.index(alpha)
                except ValueError:
                    # this is a new alpha value we haven't seen yet
                    info.alphas.append(alpha)
                    info.pos.append(pos)
                    if is_meta:
                        for req in func.needs_results:
                            if callable(req.alpha):
                                req_alpha = req.alpha(alpha)
                            else:
                                req_alpha = req.alpha
                            add_func(req.func, alpha=req_alpha)
                else:
                    # repeated alpha value
                    if pos is not None:
                        if info.pos[idx] is not None:
                            msg = "{} with alpha {} passed more than once"
                            raise ValueError(msg.format(func_name, alpha))
                        info.pos[idx] = pos

    # add functions for each spec
    for i, spec in enumerate(specs):
        func_name, alpha = (spec.split(':', 1) + [None])[:2]
        if alpha is not None:
            alpha = float(alpha)

        try:
            func = func_mapping[func_name]
        except KeyError:
            msg = "'{}' is not a known function type"
            raise ValueError(msg.format(func_name))

        needs_alpha = getattr(func, 'needs_alpha', False)
        if needs_alpha and alpha is None:
            msg = "{} needs alpha but not passed in spec '{}'"
            raise ValueError(msg.format(func_name, spec))
        elif not needs_alpha and alpha is not None:
            msg = "{} doesn't need alpha but is passed in spec '{}'"
            raise ValueError(msg.format(func_name, spec))

        add_func(func, alpha, i)

    # number things that are dependencies only
    meta_counter = itertools.count(-1, step=-1)
    for info in itertools.chain(itervalues(funcs), itervalues(metas)):
        for i, pos in enumerate(info.pos):
            if pos is None:
                info.pos[i] = next(meta_counter)

    # fill in the dependencies for metas
    for func, info in iteritems(metas):
        deps = info.deps
        assert deps == []

        for req in func.needs_results:
            f = req.func
            req_info = (metas if hasattr(f, 'needs_results') else funcs)[f]
            if req.alpha is not None:
                if callable(req.alpha):
                    req_alpha = req.alpha(info.alphas)
                else:
                    req_alpha = req.alpha

                find_alpha = np.vectorize(req_info.alphas.index, otypes=[int])
                pos = np.asarray(req_info.pos)[find_alpha(req_alpha)]
                if np.isscalar(pos):
                    deps.append(pos[()])
                else:
                    deps.extend(pos)
            else:
                pos, = req_info.pos
                deps.append(pos)

    # topological sort of metas
    meta_order = topological_sort(meta_deps)
    metas_ordered = OrderedDict(
        (f, metas[f]) for f in meta_order if hasattr(f, 'needs_results'))

    return funcs, metas_ordered, -next(meta_counter) - 1