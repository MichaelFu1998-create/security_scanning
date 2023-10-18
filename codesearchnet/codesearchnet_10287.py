def run(self, pre=None, post=None, mdrunargs=None, **mpiargs):
        """Execute the mdrun command (possibly as a MPI command) and run the simulation.

        :Keywords:
          *pre*
             a dictionary containing keyword arguments for the :meth:`prehook`
          *post*
             a dictionary containing keyword arguments for the :meth:`posthook`
          *mdrunargs*
             a dictionary with keyword arguments for :program:`mdrun` which supersede
             **and update** the defaults given to the class constructor
          *mpiargs*
             all other keyword arguments that are processed by :meth:`mpicommand`
        """

        if pre is None:
            pre = {}
        if post is None:
            post = {}
        if mdrunargs is not None:
            try:
                self.MDRUN.gmxargs.update(mdrunargs)
            except (ValueError, TypeError):
                msg = "mdrunargs must be a dict of mdrun options, not {0}".format(mdrunargs)
                logger.error(msg)
                raise

        cmd = self.commandline(**mpiargs)

        with utilities.in_dir(self.dirname, create=False):
           try:
               self.prehook(**pre)
               logger.info(" ".join(cmd))
               rc = subprocess.call(cmd)
           except:
               logger.exception("Failed MD run for unknown reasons.")
               raise
           finally:
               self.posthook(**post)
        if rc == 0:
            logger.info("MDrun completed ok, returncode = {0:d}".format(rc))
        else:
            logger.critical("Failure in MDrun, returncode = {0:d}".format(rc))
        return rc