def receive(self):
        """return a list results of all tasks.

        This method waits for all tasks to finish.

        Returns
        -------
        list
            A list of results of the tasks. The results are sorted in
            the order in which the tasks are put.

        """
        pkgidx_result_pairs = self.receive_all()
        if pkgidx_result_pairs is None:
            return
        results = [r for _, r in pkgidx_result_pairs]
        return results