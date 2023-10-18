def spawn_new_gdb_subprocess(self):
        """Spawn a new gdb subprocess with the arguments supplied to the object
        during initialization. If gdb subprocess already exists, terminate it before
        spanwing a new one.
        Return int: gdb process id
        """
        if self.gdb_process:
            self.logger.debug(
                "Killing current gdb subprocess (pid %d)" % self.gdb_process.pid
            )
            self.exit()

        self.logger.debug('Launching gdb: "%s"' % " ".join(self.cmd))

        # Use pipes to the standard streams
        self.gdb_process = subprocess.Popen(
            self.cmd,
            shell=False,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
        )

        _make_non_blocking(self.gdb_process.stdout)
        _make_non_blocking(self.gdb_process.stderr)

        # save file numbers for use later
        self.stdout_fileno = self.gdb_process.stdout.fileno()
        self.stderr_fileno = self.gdb_process.stderr.fileno()
        self.stdin_fileno = self.gdb_process.stdin.fileno()

        self.read_list = [self.stdout_fileno, self.stderr_fileno]
        self.write_list = [self.stdin_fileno]

        # string buffers for unifinished gdb output
        self._incomplete_output = {"stdout": None, "stderr": None}
        return self.gdb_process.pid