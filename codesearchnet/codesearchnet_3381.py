def run(self, procs=1, timeout=None, should_profile=False):
        """
        Runs analysis.

        :param int procs: Number of parallel worker processes
        :param timeout: Analysis timeout, in seconds
        """
        assert not self.running, "Manticore is already running."
        self._start_run()

        self._last_run_stats['time_started'] = time.time()
        with self.shutdown_timeout(timeout):
            self._start_workers(procs, profiling=should_profile)

            self._join_workers()
        self._finish_run(profiling=should_profile)