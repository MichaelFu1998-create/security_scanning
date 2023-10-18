def strip_fit(self, **kwargs):
        """Strip water and fit to the remaining system.

        First runs :meth:`strip_water` and then :meth:`fit`; see there
        for arguments.

        - *strip_input* is used for :meth:`strip_water` (but is only useful in
          special cases, e.g. when there is no Protein group defined. Then set
          *strip_input* = ``['Other']``.

        - *input* is passed on to :meth:`fit` and can contain the
          ``[center_group, fit_group, output_group]``

        - *fitgroup* is only passed to :meth:`fit` and just contains
          the group to fit to ("backbone" by default)

          .. warning:: *fitgroup* can only be a Gromacs default group and not
                       a custom group (because the indices change after stripping)

        - By default *fit* = "rot+trans" (and *fit* is passed to :meth:`fit`,
          together with the *xy* = ``False`` keyword)

        .. Note:: The call signature of :meth:`strip_water` is somewhat different from this one.
        """
        kwargs.setdefault('fit', 'rot+trans')
        kw_fit = {}
        for k in ('xy', 'fit', 'fitgroup', 'input'):
            if k in kwargs:
                kw_fit[k] = kwargs.pop(k)

        kwargs['input'] = kwargs.pop('strip_input', ['Protein'])
        kwargs['force'] = kw_fit['force'] = kwargs.pop('force', self.force)

        paths = self.strip_water(**kwargs)    # updates self.nowater
        transformer_nowater = self.nowater[paths['xtc']]  # make sure to get the one we just produced
        return transformer_nowater.fit(**kw_fit)