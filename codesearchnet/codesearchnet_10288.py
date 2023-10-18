def run_check(self, **kwargs):
        """Run :program:`mdrun` and check if run completed when it finishes.

        This works by looking at the mdrun log file for 'Finished
        mdrun on node'. It is useful to implement robust simulation
        techniques.

        :Arguments:
           *kwargs* are keyword arguments that are passed on to
           :meth:`run` (typically used for mpi things)

        :Returns:
           - ``True`` if run completed successfully
           - ``False`` otherwise
        """
        rc = None   # set to something in case we ever want to look at it later (and bomb in the try block)
        try:
            rc = self.run(**kwargs)
        except:
            logger.exception("run_check: caught exception")
        status = self.check_success()
        if status:
            logger.info("run_check: Hooray! mdrun finished successfully")
        else:
            logger.error("run_check: mdrun failed to complete run")
        return status