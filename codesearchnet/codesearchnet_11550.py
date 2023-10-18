def result_fullpath(self, package_index):
        """Returns the full path of the result

        This method returns the full path to the result. This method
        simply constructs the path based on the convention and doesn't
        check if the result actually exists.

        Parameters
        ----------
        package_index :
            a package index

        Returns
        -------
        str
            the full path to the result

        """

        ret = os.path.join(self.path, self.result_relpath(package_index))
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/results/task_00009/result.p.gz'

        return ret