def _launch_process_group(self, process_commands, streams_path):
        """
        Launches processes defined by process_commands, but only
        executes max_concurrency processes at a time; if a process
        completes and there are still outstanding processes to be
        executed, the next processes are run until max_concurrency is
        reached again.
        """
        processes = {}
        def check_complete_processes(wait=False):
            """
            Returns True if a process completed, False otherwise.
            Optionally allows waiting for better performance (avoids
            sleep-poll cycle if possible).
            """
            result = False
            # list creates copy of keys, as dict is modified in loop
            for proc in list(processes):
                if wait: proc.wait()
                if proc.poll() is not None:
                    # process is done, free up slot
                    self.debug("Process %d exited with code %d."
                               % (processes[proc]['tid'], proc.poll()))
                    processes[proc]['stdout'].close()
                    processes[proc]['stderr'].close()
                    del processes[proc]
                    result = True
            return result

        for cmd, tid in process_commands:
            self.debug("Starting process %d..." % tid)
            job_timestamp = time.strftime('%H%M%S')
            basename = "%s_%s_tid_%d" % (self.batch_name, job_timestamp, tid)
            stdout_handle = open(os.path.join(streams_path, "%s.o.%d"
                                              % (basename, tid)), "wb")
            stderr_handle = open(os.path.join(streams_path, "%s.e.%d"
                                              % (basename, tid)), "wb")
            proc = subprocess.Popen(cmd, stdout=stdout_handle, stderr=stderr_handle)
            processes[proc] = { 'tid' : tid,
                                'stdout' : stdout_handle,
                                'stderr' : stderr_handle }

            if self.max_concurrency:
                # max_concurrency reached, wait until more slots available
                while len(processes) >= self.max_concurrency:
                    if not check_complete_processes(len(processes)==1):
                        time.sleep(0.1)

        # Wait for all processes to complete
        while len(processes) > 0:
            if not check_complete_processes(True):
                time.sleep(0.1)