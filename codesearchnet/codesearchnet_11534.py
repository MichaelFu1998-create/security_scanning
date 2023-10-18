def put(self, package):
        """put a task

        This method places a task in the working area and have the
        dispatcher execute it.

        If you need to put multiple tasks, it can be much faster to
        use `put_multiple()` than to use this method multiple times
        depending of the dispatcher.

        Parameters
        ----------
        package : callable
            A task

        Returns
        -------
        int
            A package index assigned by the working area

        """

        pkgidx = self.workingArea.put_package(package)

        logger = logging.getLogger(__name__)
        logger.info('submitting {}'.format(self.workingArea.package_relpath(pkgidx)))

        runid = self.dispatcher.run(self.workingArea, pkgidx)
        self.runid_pkgidx_map[runid] = pkgidx
        return pkgidx