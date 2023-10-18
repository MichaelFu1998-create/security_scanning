def collate_and_launch(self):
        """
        Method that collates the previous jobs and launches the next
        block of concurrent jobs when using DynamicArgs. This method
        is invoked on initial launch and then subsequently via a
        commandline call (to Python via qsub) to collate the
        previously run jobs and launch the next block of jobs.
        """

        try:   specs = next(self.spec_iter)
        except StopIteration:
            self.qdel_batch()
            if self.reduction_fn is not None:
                self.reduction_fn(self._spec_log, self.root_directory)
            self._record_info()
            return

        tid_specs = [(self.last_tid + i, spec) for (i,spec) in enumerate(specs)]
        self.last_tid += len(specs)
        self._append_log(tid_specs)

        # Updating the argument specifier
        if self.dynamic:
            self.args.update(self.last_tids, self._launchinfo)
        self.last_tids = [tid for (tid,_) in tid_specs]

        output_dir = self.qsub_flag_options['-o']
        error_dir = self.qsub_flag_options['-e']
        self._qsub_block(output_dir, error_dir, tid_specs)

        # Pickle launcher before exit if necessary.
        if self.dynamic or (self.reduction_fn is not None):
            pickle_path = os.path.join(self.root_directory, 'qlauncher.pkl')
            pickle.dump(self, open(pickle_path,'wb'), protocol=2)