def build_funcs(self):
        """
        Here, we build gradient and hessian functions based on the properties
        of a state that are generally wanted. For each one, we fill in _grad or
        _hess with a function that takes care of various options such as
        slicing and flattening. For example, `m` below takes the model, selects
        different indices from it, maybe flattens it and copies it. This is
        then used in the fisherinformation, gradmodel, and hessmodel functions.
        """
        # create essentially lambda functions, but with a nice signature
        def m(inds=None, slicer=None, flat=True):
            return sample(self.model, inds=inds, slicer=slicer, flat=flat).copy()

        def r(inds=None, slicer=None, flat=True):
            return sample(self.residuals, inds=inds, slicer=slicer, flat=flat).copy()

        def l():
            return self.loglikelihood

        def r_e(**kwargs):
            """sliced etc residuals, with state.error appended on"""
            return r(**kwargs), np.copy(self.error)

        def m_e(**kwargs):
            """sliced etc residuals, with state.error appended on"""
            return m(**kwargs), np.copy(self.error)

        # set the member functions using partial
        self.fisherinformation = partial(self._jtj, funct=m)
        self.gradloglikelihood = partial(self._grad, funct=l)
        self.hessloglikelihood = partial(self._hess, funct=l)
        self.gradmodel = partial(self._grad, funct=m)
        self.hessmodel = partial(self._hess, funct=m)
        self.JTJ = partial(self._jtj, funct=r)
        self.J = partial(self._grad, funct=r)
        self.J_e = partial(self._grad, funct=r_e, nout=2)
        self.gradmodel_e = partial(self._grad, funct=m_e, nout=2)

        # add the appropriate documentation to the following functions
        self.fisherinformation.__doc__ = _graddoc + _sampledoc
        self.gradloglikelihood.__doc__ = _graddoc
        self.hessloglikelihood.__doc__ = _graddoc
        self.gradmodel.__doc__ = _graddoc + _sampledoc
        self.hessmodel.__doc__ = _graddoc + _sampledoc
        self.JTJ.__doc__ = _graddoc + _sampledoc
        self.J.__doc__ = _graddoc + _sampledoc

        # add documentation to the private functions as well. this is done
        # slightly differently, hence the function call
        self._dograddoc(self._grad_one_param)
        self._dograddoc(self._hess_two_param)
        self._dograddoc(self._grad)
        self._dograddoc(self._hess)

        # the state object is a workaround so that other interfaces still
        # work. this should probably be removed in the long run
        class _Statewrap(object):
            def __init__(self, obj):
                self.obj = obj
            def __getitem__(self, d=None):
                if d is None:
                    d = self.obj.params
                return util.delistify(self.obj.get_values(d), d)

        self.state = _Statewrap(self)