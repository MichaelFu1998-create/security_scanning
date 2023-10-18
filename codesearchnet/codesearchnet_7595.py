def plot(self, filename=None, norm=False, ylim=None,
              sides=None,  **kargs):
        """a simple plotting routine to plot the PSD versus frequency.

        :param str filename: save the figure into a file
        :param norm: False by default. If True, the PSD is normalised.
        :param ylim: readjust the y range .
        :param sides: if not provided, :attr:`sides` is used. See :attr:`sides`
            for details.
        :param kargs: any optional argument accepted by :func:`pylab.plot`.

        .. plot::
            :width: 80%
            :include-source:

            from spectrum import *
            p = Periodogram(marple_data)
            p.plot(norm=True, marker='o')

        """
        import pylab
        from pylab import ylim as plt_ylim
        #First, check that psd attribute is up-to-date
        # just to get the PSD to be recomputed if needed
        _ = self.psd


        # check that the input sides parameter is correct if provided
        if sides is not None:
            if sides not in self._sides_choices:
                raise errors.SpectrumChoiceError(sides, self._sides_choices)

        # if sides is provided but identical to the current psd, nothing to do.
        # if sides not provided, let us use self.sides
        if sides is None or sides == self.sides:
            frequencies = self.frequencies()
            psd = self.psd
            sides = self.sides
        elif sides is not None:
            # if sides argument is different from the attribute, we need to
            # create a new PSD/Freq ; indeed we do not want to change the
            # attribute itself

            # if data is complex, one-sided is wrong in any case.
            if self.datatype == 'complex':
                if sides == 'onesided':
                    raise ValueError("sides cannot be one-sided with complex data")

            logging.debug("sides is different from the one provided. Converting PSD")
            frequencies = self.frequencies(sides=sides)
            psd = self.get_converted_psd(sides)

        if len(psd) != len(frequencies):
            raise ValueError("PSD length is %s and freq length is %s" % (len(psd), len(frequencies)))

        if 'ax' in list(kargs.keys()):
            save_ax = pylab.gca()
            pylab.sca(kargs['ax'])
            rollback = True
            del kargs['ax']
        else:
            rollback = False

        if norm:
            pylab.plot(frequencies, 10 * stools.log10(psd/max(psd)),  **kargs)
        else:
            pylab.plot(frequencies, 10 * stools.log10(psd),**kargs)

        pylab.xlabel('Frequency')
        pylab.ylabel('Power (dB)')
        pylab.grid(True)

        if ylim:
            plt_ylim(ylim)

        if sides == 'onesided':
            pylab.xlim(0, self.sampling/2.)
        elif sides == 'twosided':
            pylab.xlim(0, self.sampling)
        elif sides == 'centerdc':
            pylab.xlim(-self.sampling/2., self.sampling/2.)

        if filename:
            pylab.savefig(filename)

        if rollback:
            pylab.sca(save_ax)

        del psd, frequencies