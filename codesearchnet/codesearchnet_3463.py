def load(self, filename, env):
        """
        Loads and an ELF program in memory and prepares the initial CPU state.
        Creates the stack and loads the environment variables and the arguments in it.

        :param filename: pathname of the file to be executed. (used for auxv)
        :param list env: A list of env variables. (used for extracting vars that control ld behavior)
        :raises error:
            - 'Not matching cpu': if the program is compiled for a different architecture
            - 'Not matching memory': if the program is compiled for a different address size
        :todo: define va_randomize and read_implies_exec personality
        """
        # load elf See binfmt_elf.c
        # read the ELF object file
        cpu = self.current
        elf = self.elf
        arch = self.arch
        env = dict(var.split('=') for var in env if '=' in var)
        addressbitsize = {'x86': 32, 'x64': 64, 'ARM': 32}[elf.get_machine_arch()]
        logger.debug("Loading %s as a %s elf", filename, arch)

        assert elf.header.e_type in ['ET_DYN', 'ET_EXEC', 'ET_CORE']

        # Get interpreter elf
        interpreter = None
        for elf_segment in elf.iter_segments():
            if elf_segment.header.p_type != 'PT_INTERP':
                continue
            interpreter_filename = elf_segment.data()[:-1]
            logger.info(f'Interpreter filename: {interpreter_filename}')
            if os.path.exists(interpreter_filename.decode('utf-8')):
                interpreter = ELFFile(open(interpreter_filename, 'rb'))
            elif 'LD_LIBRARY_PATH' in env:
                for mpath in env['LD_LIBRARY_PATH'].split(":"):
                    interpreter_path_filename = os.path.join(mpath, os.path.basename(interpreter_filename))
                    logger.info(f"looking for interpreter {interpreter_path_filename}")
                    if os.path.exists(interpreter_path_filename):
                        interpreter = ELFFile(open(interpreter_path_filename, 'rb'))
                        break
            break
        if interpreter is not None:
            assert interpreter.get_machine_arch() == elf.get_machine_arch()
            assert interpreter.header.e_type in ['ET_DYN', 'ET_EXEC']

        # Stack Executability
        executable_stack = False
        for elf_segment in elf.iter_segments():
            if elf_segment.header.p_type != 'PT_GNU_STACK':
                continue
            if elf_segment.header.p_flags & 0x01:
                executable_stack = True
            else:
                executable_stack = False
            break

        base = 0
        elf_bss = 0
        end_code = 0
        end_data = 0
        elf_brk = 0
        self.load_addr = 0

        for elf_segment in elf.iter_segments():
            if elf_segment.header.p_type != 'PT_LOAD':
                continue

            align = 0x1000  # elf_segment.header.p_align

            ELF_PAGEOFFSET = elf_segment.header.p_vaddr & (align - 1)

            flags = elf_segment.header.p_flags
            memsz = elf_segment.header.p_memsz + ELF_PAGEOFFSET
            offset = elf_segment.header.p_offset - ELF_PAGEOFFSET
            filesz = elf_segment.header.p_filesz + ELF_PAGEOFFSET
            vaddr = elf_segment.header.p_vaddr - ELF_PAGEOFFSET
            memsz = cpu.memory._ceil(memsz)
            if base == 0 and elf.header.e_type == 'ET_DYN':
                assert vaddr == 0
                if addressbitsize == 32:
                    base = 0x56555000
                else:
                    base = 0x555555554000

            perms = perms_from_elf(flags)
            hint = base + vaddr
            if hint == 0:
                hint = None

            logger.debug(f"Loading elf offset: {offset:08x} addr:{base + vaddr:08x} {base + vaddr + memsz:08x} {perms}")
            base = cpu.memory.mmapFile(hint, memsz, perms, elf_segment.stream.name, offset) - vaddr

            if self.load_addr == 0:
                self.load_addr = base + vaddr

            k = base + vaddr + filesz
            if k > elf_bss:
                elf_bss = k
            if (flags & 4) and end_code < k:  # PF_X
                end_code = k
            if end_data < k:
                end_data = k
            k = base + vaddr + memsz
            if k > elf_brk:
                elf_brk = k

        elf_entry = elf.header.e_entry
        if elf.header.e_type == 'ET_DYN':
            elf_entry += self.load_addr
        entry = elf_entry
        real_elf_brk = elf_brk

        # We need to explicitly clear bss, as fractional pages will have data from the file
        bytes_to_clear = elf_brk - elf_bss
        if bytes_to_clear > 0:
            logger.debug(f"Zeroing main elf fractional pages. From bss({elf_bss:x}) to brk({elf_brk:x}), {bytes_to_clear} bytes.")
            cpu.write_bytes(elf_bss, '\x00' * bytes_to_clear, force=True)

        stack_size = 0x21000

        if addressbitsize == 32:
            stack_top = 0xc0000000
        else:
            stack_top = 0x800000000000
        stack_base = stack_top - stack_size
        stack = cpu.memory.mmap(stack_base, stack_size, 'rwx', name='stack') + stack_size
        assert stack_top == stack

        reserved = cpu.memory.mmap(base + vaddr + memsz, 0x1000000, '   ')
        interpreter_base = 0
        if interpreter is not None:
            base = 0
            elf_bss = 0
            end_code = 0
            end_data = 0
            elf_brk = 0
            entry = interpreter.header.e_entry
            for elf_segment in interpreter.iter_segments():
                if elf_segment.header.p_type != 'PT_LOAD':
                    continue
                align = 0x1000  # elf_segment.header.p_align
                vaddr = elf_segment.header.p_vaddr
                filesz = elf_segment.header.p_filesz
                flags = elf_segment.header.p_flags
                offset = elf_segment.header.p_offset
                memsz = elf_segment.header.p_memsz

                ELF_PAGEOFFSET = (vaddr & (align - 1))
                memsz = memsz + ELF_PAGEOFFSET
                offset = offset - ELF_PAGEOFFSET
                filesz = filesz + ELF_PAGEOFFSET
                vaddr = vaddr - ELF_PAGEOFFSET
                memsz = cpu.memory._ceil(memsz)

                if base == 0 and interpreter.header.e_type == 'ET_DYN':
                    assert vaddr == 0
                    total_size = self._interp_total_size(interpreter)
                    base = stack_base - total_size

                if base == 0:
                    assert vaddr == 0
                perms = perms_from_elf(flags)
                hint = base + vaddr
                if hint == 0:
                    hint = None

                base = cpu.memory.mmapFile(hint, memsz, perms, elf_segment.stream.name, offset)
                base -= vaddr
                logger.debug(
                    f"Loading interpreter offset: {offset:08x} "
                    f"addr:{base + vaddr:08x} "
                    f"{base + vaddr + memsz:08x} "
                    f"{(flags & 1 and 'r' or ' ')}"
                    f"{(flags & 2 and 'w' or ' ')}"
                    f"{(flags & 4 and 'x' or ' ')}"
                )

                k = base + vaddr + filesz
                if k > elf_bss:
                    elf_bss = k
                if (flags & 4) and end_code < k:  # PF_X
                    end_code = k
                if end_data < k:
                    end_data = k
                k = base + vaddr + memsz
                if k > elf_brk:
                    elf_brk = k

            if interpreter.header.e_type == 'ET_DYN':
                entry += base
            interpreter_base = base

            bytes_to_clear = elf_brk - elf_bss
            if bytes_to_clear > 0:
                logger.debug(f"Zeroing interpreter elf fractional pages. From bss({elf_bss:x}) to brk({elf_brk:x}), {bytes_to_clear} bytes.")
                cpu.write_bytes(elf_bss, '\x00' * bytes_to_clear, force=True)

        # free reserved brk space
        cpu.memory.munmap(reserved, 0x1000000)

        # load vdso
        #vdso_addr = load_vdso(addressbitsize)

        cpu.STACK = stack
        cpu.PC = entry

        logger.debug(f"Entry point: {entry:016x}")
        logger.debug(f"Stack start: {stack:016x}")
        logger.debug(f"Brk: {real_elf_brk:016x}")
        logger.debug(f"Mappings:")
        for m in str(cpu.memory).split('\n'):
            logger.debug(f"  {m}")
        self.base = base
        self.elf_bss = elf_bss
        self.end_code = end_code
        self.end_data = end_data
        self.elf_brk = real_elf_brk
        self.brk = real_elf_brk

        at_random = cpu.push_bytes('A' * 16)
        at_execfn = cpu.push_bytes(f'{filename}\x00')

        self.auxv = {
            'AT_PHDR': self.load_addr + elf.header.e_phoff,  # Program headers for program
            'AT_PHENT': elf.header.e_phentsize,       # Size of program header entry
            'AT_PHNUM': elf.header.e_phnum,           # Number of program headers
            'AT_PAGESZ': cpu.memory.page_size,         # System page size
            'AT_BASE': interpreter_base,             # Base address of interpreter
            'AT_FLAGS': elf.header.e_flags,           # Flags
            'AT_ENTRY': elf_entry,                    # Entry point of program
            'AT_UID': 1000,                         # Real uid
            'AT_EUID': 1000,                         # Effective uid
            'AT_GID': 1000,                         # Real gid
            'AT_EGID': 1000,                         # Effective gid
            'AT_CLKTCK': 100,                          # Frequency of times()
            'AT_HWCAP': 0,                            # Machine-dependent hints about processor capabilities.
            'AT_RANDOM': at_random,                    # Address of 16 random bytes.
            'AT_EXECFN': at_execfn,                    # Filename of executable.
        }