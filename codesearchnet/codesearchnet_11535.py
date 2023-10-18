def put_multiple(self, packages):
        """put tasks

        This method places multiple tasks in the working area and have
        the dispatcher execute them.

        Parameters
        ----------
        packages : list(callable)
            A list of tasks

        Returns
        -------
        list(int)
            Package indices assigned by the working area

        """

        pkgidxs = [self.workingArea.put_package(p) for p in packages]

        logger = logging.getLogger(__name__)
        logger.info('submitting {}'.format(
            ', '.join(['{}'.format(self.workingArea.package_relpath(i)) for i in pkgidxs])
        ))

        runids = self.dispatcher.run_multiple(self.workingArea, pkgidxs)
        self.runid_pkgidx_map.update(zip(runids, pkgidxs))
        return pkgidxs