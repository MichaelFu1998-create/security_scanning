def collect_result(self, package_index):
        """Collect the result of a task

        Parameters
        ----------
        package_index :
            a package index

        Returns
        -------
        obj
            The result of the task

        """

        result_fullpath = self.result_fullpath(package_index)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/results/task_00009/result.p.gz'

        try:
            with gzip.open(result_fullpath, 'rb') as f:
                result = pickle.load(f)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.warning(e)
            return None

        return result