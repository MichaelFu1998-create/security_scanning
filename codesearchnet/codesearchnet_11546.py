def put_package(self, package):
        """Put a package

        Parameters
        ----------
        package :
            a task package

        Returns
        -------
        int
            A package index

        """

        self.last_package_index += 1
        package_index = self.last_package_index

        package_fullpath = self.package_fullpath(package_index)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/task_00009.p.gz'

        with gzip.open(package_fullpath, 'wb') as f:
            pickle.dump(package, f, protocol=pickle.HIGHEST_PROTOCOL)
            f.close()

        result_fullpath = self.result_fullpath(package_index)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/results/task_00009/result.p.gz'

        result_dir = os.path.dirname(result_fullpath)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/results/task_00009'

        alphatwirl.mkdir_p(result_dir)

        return package_index