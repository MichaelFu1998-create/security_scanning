def setup_stack(self, argv, envp):
        """
        :param Cpu cpu: The cpu instance
        :param argv: list of parameters for the program to execute.
        :param envp: list of environment variables for the program to execute.

        http://www.phrack.org/issues.html?issue=58&id=5#article
         position            content                     size (bytes) + comment
         ----------------------------------------------------------------------
         stack pointer ->  [ argc = number of args ]     4
                         [ argv[0] (pointer) ]         4   (program name)
                         [ argv[1] (pointer) ]         4
                         [ argv[..] (pointer) ]        4 * x
                         [ argv[n - 1] (pointer) ]     4
                         [ argv[n] (pointer) ]         4   (= NULL)

                         [ envp[0] (pointer) ]         4
                         [ envp[1] (pointer) ]         4
                         [ envp[..] (pointer) ]        4
                         [ envp[term] (pointer) ]      4   (= NULL)

                         [ auxv[0] (Elf32_auxv_t) ]    8
                         [ auxv[1] (Elf32_auxv_t) ]    8
                         [ auxv[..] (Elf32_auxv_t) ]   8
                         [ auxv[term] (Elf32_auxv_t) ] 8   (= AT_NULL vector)

                         [ padding ]                   0 - 16

                         [ argument ASCIIZ strings ]   >= 0
                         [ environment ASCIIZ str. ]   >= 0

         (0xbffffffc)      [ end marker ]                4   (= NULL)

         (0xc0000000)      < top of stack >              0   (virtual)
         ----------------------------------------------------------------------
        """
        cpu = self.current

        # In case setup_stack() is called again, we make sure we're growing the
        # stack from the original top
        cpu.STACK = self._stack_top

        auxv = self.auxv
        logger.debug("Setting argv, envp and auxv.")
        logger.debug(f"\tArguments: {argv!r}")
        if envp:
            logger.debug("\tEnvironment:")
            for e in envp:
                logger.debug(f"\t\t{e!r}")

        logger.debug("\tAuxv:")
        for name, val in auxv.items():
            logger.debug(f"\t\t{name}: 0x{val:x}")

        # We save the argument and environment pointers
        argvlst = []
        envplst = []

        # end envp marker empty string
        for evar in envp:
            cpu.push_bytes('\x00')
            envplst.append(cpu.push_bytes(evar))

        for arg in argv:
            cpu.push_bytes('\x00')
            argvlst.append(cpu.push_bytes(arg))

        # Put all auxv strings into the string stack area.
        # And replace the value be its pointer

        for name, value in auxv.items():
            if hasattr(value, '__len__'):
                cpu.push_bytes(value)
                auxv[name] = cpu.STACK

        # The "secure execution" mode of secure_getenv() is controlled by the
        # AT_SECURE flag contained in the auxiliary vector passed from the
        # kernel to user space.
        auxvnames = {
            'AT_IGNORE': 1,  # Entry should be ignored
            'AT_EXECFD': 2,  # File descriptor of program
            'AT_PHDR': 3,  # Program headers for program
            'AT_PHENT': 4,  # Size of program header entry
            'AT_PHNUM': 5,  # Number of program headers
            'AT_PAGESZ': 6,  # System page size
            'AT_BASE': 7,  # Base address of interpreter
            'AT_FLAGS': 8,  # Flags
            'AT_ENTRY': 9,  # Entry point of program
            'AT_NOTELF': 10,  # Program is not ELF
            'AT_UID': 11,  # Real uid
            'AT_EUID': 12,  # Effective uid
            'AT_GID': 13,  # Real gid
            'AT_EGID': 14,  # Effective gid
            'AT_CLKTCK': 17,  # Frequency of times()
            'AT_PLATFORM': 15,  # String identifying platform.
            'AT_HWCAP': 16,  # Machine-dependent hints about processor capabilities.
            'AT_FPUCW': 18,  # Used FPU control word.
            'AT_SECURE': 23,  # Boolean, was exec setuid-like?
            'AT_BASE_PLATFORM': 24,  # String identifying real platforms.
            'AT_RANDOM': 25,  # Address of 16 random bytes.
            'AT_EXECFN': 31,  # Filename of executable.
            'AT_SYSINFO': 32,  # Pointer to the global system page used for system calls and other nice things.
            'AT_SYSINFO_EHDR': 33,  # Pointer to the global system page used for system calls and other nice things.
        }
        # AT_NULL
        cpu.push_int(0)
        cpu.push_int(0)
        for name, val in auxv.items():
            cpu.push_int(val)
            cpu.push_int(auxvnames[name])

        # NULL ENVP
        cpu.push_int(0)
        for var in reversed(envplst):              # ENVP n
            cpu.push_int(var)
        envp = cpu.STACK

        # NULL ARGV
        cpu.push_int(0)
        for arg in reversed(argvlst):              # Argv n
            cpu.push_int(arg)
        argv = cpu.STACK

        # ARGC
        cpu.push_int(len(argvlst))