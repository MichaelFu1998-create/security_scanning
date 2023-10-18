def center_fit(self, **kwargs):
        """Write compact xtc that is fitted to the tpr reference structure.

        See :func:`gromacs.cbook.trj_fitandcenter` for details and
        description of *kwargs* (including *input*, *input1*, *n* and
        *n1* for how to supply custom index groups). The most important ones are listed
        here but in most cases the defaults should work.

        :Keywords:
           *s*
             Input structure (typically the default tpr file but can be set to
             some other file with a different conformation for fitting)
           *n*
             Alternative index file.
           *o*
             Name of the output trajectory.
           *xy* : Boolean
             If ``True`` then only fit in xy-plane (useful for a membrane normal
             to z). The default is ``False``.
           *force*
             - ``True``: overwrite existing trajectories
             - ``False``: throw a IOError exception
             - ``None``: skip existing and log a warning [default]

        :Returns:
              dictionary with keys *tpr*, *xtc*, which are the names of the
              the new files
        """
        kwargs.setdefault('s', self.tpr)
        kwargs.setdefault('n', self.ndx)
        kwargs['f'] = self.xtc
        kwargs.setdefault('o', self.outfile(self.infix_filename(None, self.xtc, '_centfit', 'xtc')))
        force = kwargs.pop('force', self.force)

        logger.info("Centering and fitting trajectory {f!r}...".format(**kwargs))
        with utilities.in_dir(self.dirname):
            if not self.check_file_exists(kwargs['o'], resolve="indicate", force=force):
                trj_fitandcenter(**kwargs)
            logger.info("Centered and fit trajectory: {o!r}.".format(**kwargs))
        return {'tpr': self.rp(kwargs['s']), 'xtc': self.rp(kwargs['o'])}