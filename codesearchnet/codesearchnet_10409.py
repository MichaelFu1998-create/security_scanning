def set_correlparameters(self, **kwargs):
        """Set and change the parameters for calculations with  correlation functions.

        The parameters persist until explicitly changed.

        :Keywords:
           *nstep*
               only process every *nstep* data point to speed up the FFT; if
               left empty a default is chosen that produces roughly 25,000 data
               points (or whatever is set in *ncorrel*)
           *ncorrel*
               If no *nstep* is supplied, aim at using *ncorrel* data points for
               the FFT; sets :attr:`XVG.ncorrel` [25000]
           *force*
               force recalculating correlation data even if cached values are
               available
           *kwargs*
               see :func:`numkit.timeseries.tcorrel` for other options

        .. SeeAlso: :attr:`XVG.error` for details and references.
        """
        self.ncorrel = kwargs.pop('ncorrel', self.ncorrel) or 25000
        nstep = kwargs.pop('nstep', None)
        if nstep is None:
            # good step size leads to ~25,000 data points
            nstep = len(self.array[0])/float(self.ncorrel)
            nstep = int(numpy.ceil(nstep))  # catch small data sets
        kwargs['nstep'] = nstep
        self.__correlkwargs.update(kwargs)  # only contains legal kw for numkit.timeseries.tcorrel or force
        return self.__correlkwargs