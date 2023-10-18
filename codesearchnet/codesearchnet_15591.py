def open(self):
        """ Daemonize this process

        Do everything that is needed to become a Unix daemon.

        :return: None
        :raise: DaemonError
        """
        if self.is_open:
            return
        try:
            os.chdir(self.working_directory)
            if self.chroot_directory:
                os.chroot(self.chroot_directory)
            os.setgid(self.gid)
            os.setuid(self.uid)
            os.umask(self.umask)
        except OSError as err:
            raise DaemonError('Setting up Environment failed: {0}'
                              .format(err))

        if self.prevent_core:
            try:
                resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
            except Exception as err:
                raise DaemonError('Could not disable core files: {0}'
                                  .format(err))

        if self.detach_process:
            try:
                if os.fork() > 0:
                    os._exit(0)
            except OSError as err:
                raise DaemonError('First fork failed: {0}'.format(err))
            os.setsid()
            try:
                if os.fork() > 0:
                    os._exit(0)
            except OSError as err:
                raise DaemonError('Second fork failed: {0}'.format(err))

        for (signal_number, handler) in self._signal_handler_map.items():
            signal.signal(signal_number, handler)

        close_filenos(self._files_preserve)

        redirect_stream(sys.stdin, self.stdin)
        redirect_stream(sys.stdout, self.stdout)
        redirect_stream(sys.stderr, self.stderr)

        if self.pidfile:
            self.pidfile.acquire()

        self._is_open = True