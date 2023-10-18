def _launch_process_group(self, process_commands, streams_path):
        """
        Aggregates all process_commands and the designated output files into a
        list, and outputs it as JSON, after which the wrapper script is called.
        """
        processes = []
        for cmd, tid in process_commands:
            job_timestamp = time.strftime('%H%M%S')
            basename = "%s_%s_tid_%d" % (self.batch_name, job_timestamp, tid)
            stdout_path = os.path.join(streams_path, "%s.o.%d" % (basename, tid))
            stderr_path = os.path.join(streams_path, "%s.e.%d" % (basename, tid))
            process = { 'tid' : tid,
                        'cmd' : cmd,
                        'stdout' : stdout_path,
                        'stderr' : stderr_path }
            processes.append(process)

        # To make the JSON filename unique per group, we use the last tid in
        # this group.
        json_path = os.path.join(self.root_directory, self.json_name % (tid))
        with open(json_path, 'w') as json_file:
            json.dump(processes, json_file, sort_keys=True, indent=4)

        p = subprocess.Popen([self.script_path, json_path, self.batch_name,
                              str(len(processes)), str(self.max_concurrency)])
        if p.wait() != 0:
            raise EnvironmentError("Script command exit with code: %d" % p.poll())