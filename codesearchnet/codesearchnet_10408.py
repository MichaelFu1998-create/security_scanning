def _tcorrel(self, nstep=100, **kwargs):
        """Correlation "time" of data.

        The 0-th column of the data is interpreted as a time and the
        decay of the data is computed from the autocorrelation
        function (using FFT).

        .. SeeAlso:: :func:`numkit.timeseries.tcorrel`
        """
        t = self.array[0,::nstep]
        r = gromacs.collections.Collection([numkit.timeseries.tcorrel(t, Y, nstep=1, **kwargs) for Y in self.array[1:,::nstep]])
        return r