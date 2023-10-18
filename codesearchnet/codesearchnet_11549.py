def result_relpath(self, package_index):
        """Returns the relative path of the result

        This method returns the path to the result relative to the
        top dir of the working area. This method simply constructs the
        path based on the convention and doesn't check if the result
        actually exists.

        Parameters
        ----------
        package_index :
            a package index

        Returns
        -------
        str
            the relative path to the result

        """

        dirname = 'task_{:05d}'.format(package_index)
        # e.g., 'task_00009'

        ret = os.path.join('results', dirname, 'result.p.gz')
        # e.g., 'results/task_00009/result.p.gz'

        return ret