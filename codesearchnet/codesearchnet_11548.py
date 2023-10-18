def package_fullpath(self, package_index):
        """Returns the full path of the package

        This method returns the full path to the package. This method
        simply constructs the path based on the convention and doesn't
        check if the package actually exists.

        Parameters
        ----------
        package_index :
            a package index

        Returns
        -------
        str
            the full path to the package

        """

        ret = os.path.join(self.path, self.package_relpath(package_index))
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/task_00009.p.gz'

        return ret