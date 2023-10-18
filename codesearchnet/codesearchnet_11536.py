def receive(self):
        """return pairs of package indices and results of all tasks

        This method waits until all tasks finish.

        Returns
        -------
        list
            A list of pairs of package indices and results

        """

        ret = [ ] # a list of (pkgid, result)
        while True:

            if self.runid_pkgidx_map:
                self.runid_to_return.extend(self.dispatcher.poll())
                ret.extend(self._collect_all_finished_pkgidx_result_pairs())

            if not self.runid_pkgidx_map:
                break
            time.sleep(self.sleep)

        ret = sorted(ret, key=itemgetter(0))

        return ret