def _execve(self, program, argv, envp):
        """
        Load `program` and establish program state, such as stack and arguments.

        :param program str: The ELF binary to load
        :param argv list: argv array
        :param envp list: envp array
        """
        argv = [] if argv is None else argv
        envp = [] if envp is None else envp

        logger.debug(f"Loading {program} as a {self.arch} elf")

        self.load(program, envp)
        self._arch_specific_init()

        self._stack_top = self.current.STACK
        self.setup_stack([program] + argv, envp)

        nprocs = len(self.procs)
        nfiles = len(self.files)
        assert nprocs > 0
        self.running = list(range(nprocs))

        # Each process can wait for one timeout
        self.timers = [None] * nprocs
        # each fd has a waitlist
        self.rwait = [set() for _ in range(nfiles)]
        self.twait = [set() for _ in range(nfiles)]

        # Install event forwarders
        for proc in self.procs:
            self.forward_events_from(proc)