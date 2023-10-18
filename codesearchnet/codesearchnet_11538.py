def receive_one(self):
        """return a pair of a package index and result of a task

        This method waits until a tasks finishes. It returns `None` if
        no task is running.

        Returns
        -------
        tuple or None
            A pair of a package index and result. `None` if no tasks
            is running.

        """

        if not self.runid_pkgidx_map:
            return None

        while True:

            if not self.runid_to_return:
                self.runid_to_return.extend(self.dispatcher.poll())

            ret = self._collect_next_finished_pkgidx_result_pair()

            if ret is not None:
                break

            if self.runid_pkgidx_map:
                time.sleep(self.sleep)

        return ret