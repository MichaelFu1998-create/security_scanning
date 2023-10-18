def strip_water(self, os=None, o=None, on=None, compact=False,
                    resn="SOL", groupname="notwater", **kwargs):
        """Write xtc and tpr with water (by resname) removed.

        :Keywords:
           *os*
              Name of the output tpr file; by default use the original but
              insert "nowater" before suffix.
           *o*
              Name of the output trajectory; by default use the original name but
              insert "nowater" before suffix.
           *on*
              Name of a new index file (without water).
           *compact*
              ``True``: write a compact and centered trajectory
              ``False``: use trajectory as it is [``False``]
           *centergroup*
              Index group used for centering ["Protein"]

              .. Note:: If *input* is provided (see below under *kwargs*)
                        then *centergroup* is ignored and the group for
                        centering is taken as the first entry in *input*.

           *resn*
              Residue name of the water molecules; all these residues are excluded.
           *groupname*
              Name of the group that is generated by subtracting all waters
              from the system.
           *force* : Boolean
             - ``True``: overwrite existing trajectories
             - ``False``: throw a IOError exception
             - ``None``: skip existing and log a warning [default]
           *kwargs*
              are passed on to :func:`gromacs.cbook.trj_compact` (unless the
              values have to be set to certain values such as s, f, n, o
              keywords). The *input* keyword is always mangled: Only the first
              entry (the group to centre the trajectory on) is kept, and as a
              second group (the output group) *groupname* is used.

        :Returns:
              dictionary with keys *tpr*, *xtc*, *ndx* which are the names of the
              the new files

        .. warning:: The input tpr file should *not* have *any position restraints*;
                     otherwise Gromacs will throw a hissy-fit and say

                     *Software inconsistency error: Position restraint coordinates are
                     missing*

                     (This appears to be a bug in Gromacs 4.x.)
        """
        force = kwargs.pop('force', self.force)

        newtpr = self.outfile(self.infix_filename(os, self.tpr, '_nowater'))
        newxtc = self.outfile(self.infix_filename(o, self.xtc, '_nowater'))
        newndx = self.outfile(self.infix_filename(on, self.tpr, '_nowater', 'ndx'))

        nowater_ndx = self._join_dirname(newtpr, "nowater.ndx")    # refers to original tpr

        if compact:
            TRJCONV = trj_compact
            # input overrides centergroup
            if kwargs.get('centergroup') is not None and 'input' in kwargs:
                logger.warn("centergroup = %r will be superceded by input[0] = %r", kwargs['centergroup'], kwargs['input'][0])
            _input = kwargs.get('input', [kwargs.get('centergroup', 'Protein')])
            kwargs['input'] = [_input[0], groupname]  # [center group, write-out selection]
            del _input
            logger.info("Creating a compact trajectory centered on group %r", kwargs['input'][0])
            logger.info("Writing %r to the output trajectory", kwargs['input'][1])
        else:
            TRJCONV = gromacs.trjconv
            kwargs['input'] = [groupname]
            logger.info("Writing %r to the output trajectory (no centering)", kwargs['input'][0])
        # clean kwargs, only legal arguments for Gromacs tool trjconv should remain
        kwargs.pop("centergroup", None)

        NOTwater = "! r {resn!s}".format(**vars())  # make_ndx selection ("not water residues")
        with utilities.in_dir(self.dirname):
            # ugly because I cannot break from the block
            if not self.check_file_exists(newxtc, resolve="indicate", force=force):
                # make no-water index
                B = IndexBuilder(struct=self.tpr, selections=['@'+NOTwater],
                                 ndx=self.ndx, out_ndx=nowater_ndx)
                B.combine(name_all=groupname, operation="|", defaultgroups=True)
                logger.debug("Index file for water removal: %r", nowater_ndx)

                logger.info("TPR file without water {newtpr!r}".format(**vars()))
                gromacs.tpbconv(s=self.tpr, o=newtpr, n=nowater_ndx, input=[groupname])

                logger.info("NDX of the new system %r", newndx)
                gromacs.make_ndx(f=newtpr, o=newndx, input=['q'], stderr=False, stdout=False)
                # PROBLEM: If self.ndx contained a custom group required for fitting then we are loosing
                #          this group here. We could try to merge only this group but it is possible that
                #          atom indices changed. The only way to solve this is to regenerate the group with
                #          a selection or only use Gromacs default groups.

                logger.info("Trajectory without water {newxtc!r}".format(**vars()))
                kwargs['s'] = self.tpr
                kwargs['f'] = self.xtc
                kwargs['n'] = nowater_ndx
                kwargs['o'] = newxtc
                TRJCONV(**kwargs)

                logger.info("pdb and gro for visualization")
                for ext in 'pdb', 'gro':
                    try:
                        # see warning in doc ... so we don't use the new xtc but the old one
                        kwargs['o'] = self.filename(newtpr, ext=ext)
                        TRJCONV(dump=0, stdout=False, stderr=False, **kwargs)  # silent
                    except:
                        logger.exception("Failed building the water-less %(ext)s. "
                                         "Position restraints in tpr file (see docs)?" % vars())
            logger.info("strip_water() complete")

        self.nowater[self.rp(newxtc)] = Transformer(dirname=self.dirname, s=newtpr,
                                           f=newxtc, n=newndx, force=force)
        return {'tpr':self.rp(newtpr), 'xtc':self.rp(newxtc), 'ndx':self.rp(newndx)}