def poll(self):
        """return pairs of package indices and results of finished tasks

        This method does not wait for tasks to finish.

        Returns
        -------
        list
            A list of pairs of package indices and results

        """

        self.runid_to_return.extend(self.dispatcher.poll())
        ret = self._collect_all_finished_pkgidx_result_pairs()
        return ret