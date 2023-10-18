def fit(self, xy=False, **kwargs):
        """Write xtc that is fitted to the tpr reference structure.

        Runs :class:`gromacs.tools.trjconv` with appropriate arguments
        for fitting. The most important *kwargs* are listed
        here but in most cases the defaults should work.

        Note that the default settings do *not* include centering or
        periodic boundary treatment as this often does not work well
        with fitting. It is better to do this as a separate step (see
        :meth:`center_fit` or :func:`gromacs.cbook.trj_fitandcenter`)

        :Keywords:
           *s*
             Input structure (typically the default tpr file but can be set to
             some other file with a different conformation for fitting)
           *n*
             Alternative index file.
           *o*
             Name of the output trajectory. A default name is created.
             If e.g. *dt* = 100  is one of the *kwargs* then the default name includes
             "_dt100ps".
          *xy* : boolean
             If ``True`` then only do a rot+trans fit in the xy plane
             (good for membrane simulations); default is ``False``.
          *force*
            ``True``: overwrite existing trajectories
            ``False``: throw a IOError exception
            ``None``: skip existing and log a warning [default]
          *fitgroup*
            index group to fit on ["backbone"]

            .. Note:: If keyword *input* is supplied then it will override
                      *fitgroup*; *input* = ``[fitgroup, outgroup]``
          *kwargs*
             kwargs are passed to :func:`~gromacs.cbook.trj_xyfitted`

        :Returns:
              dictionary with keys *tpr*, *xtc*, which are the names of the
              the new files
        """
        kwargs.setdefault('s', self.tpr)
        kwargs.setdefault('n', self.ndx)
        kwargs['f'] = self.xtc
        force = kwargs.pop('force', self.force)
        if xy:
            fitmode = 'rotxy+transxy'
            kwargs.pop('fit', None)
            infix_default = '_fitxy'
        else:
            fitmode = kwargs.pop('fit', 'rot+trans')  # user can use 'progressive', too
            infix_default = '_fit'

        dt = kwargs.get('dt')
        if dt:
            infix_default += '_dt{0:d}ps'.format(int(dt))    # dt in ps

        kwargs.setdefault('o', self.outfile(self.infix_filename(None, self.xtc, infix_default, 'xtc')))
        fitgroup = kwargs.pop('fitgroup', 'backbone')
        kwargs.setdefault('input', [fitgroup, "system"])

        if kwargs.get('center', False):
            logger.warn("Transformer.fit(): center=%(center)r used: centering should not be combined with fitting.", kwargs)
            if len(kwargs['inputs']) != 3:
                logger.error("If you insist on centering you must provide three groups in the 'input' kwarg: (center, fit, output)")
                raise ValuError("Insufficient index groups for centering,fitting,output")

        logger.info("Fitting trajectory %r to with xy=%r...", kwargs['f'], xy)
        logger.info("Fitting on index group %(fitgroup)r", vars())
        with utilities.in_dir(self.dirname):
            if self.check_file_exists(kwargs['o'], resolve="indicate", force=force):
                logger.warn("File %r exists; force regenerating it with force=True.", kwargs['o'])
            else:
                gromacs.trjconv(fit=fitmode, **kwargs)
                logger.info("Fitted trajectory (fitmode=%s): %r.", fitmode, kwargs['o'])
        return {'tpr': self.rp(kwargs['s']), 'xtc': self.rp(kwargs['o'])}