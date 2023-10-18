def pool(self):
        """Return the multiprocessing.Pool instance or create it if not done yet.

        Returns
        -------
        multiprocessing.Pool
            The multiprocessing.Pool used internally by this imgaug.multicore.Pool.

        """
        if self._pool is None:
            processes = self.processes
            if processes is not None and processes < 0:
                try:
                    # cpu count includes the hyperthreads, e.g. 8 for 4 cores + hyperthreading
                    processes = multiprocessing.cpu_count() - abs(processes)
                    processes = max(processes, 1)
                except (ImportError, NotImplementedError):
                    processes = None

            self._pool = multiprocessing.Pool(processes,
                                              initializer=_Pool_initialize_worker,
                                              initargs=(self.augseq, self.seed),
                                              maxtasksperchild=self.maxtasksperchild)
        return self._pool