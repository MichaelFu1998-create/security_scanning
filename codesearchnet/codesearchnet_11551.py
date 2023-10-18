def run_multiple(self, workingArea, package_indices):
        """Submit multiple jobs

        Parameters
        ----------
        workingArea :
            A workingArea
        package_indices : list(int)
            A list of package indices

        Returns
        -------
        list(str)
            The list of the run IDs of the jobs

        """

        if not package_indices:
            return [ ]

        job_desc = self._compose_job_desc(workingArea, package_indices)

        clusterprocids = submit_jobs(job_desc, cwd=workingArea.path)

        # TODO: make configurable
        clusterids = clusterprocids2clusterids(clusterprocids)
        for clusterid in clusterids:
            change_job_priority([clusterid], 10)

        self.clusterprocids_outstanding.extend(clusterprocids)

        return clusterprocids