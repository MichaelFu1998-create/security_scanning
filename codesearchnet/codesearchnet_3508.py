def load(self, filename):
        """
        Loads a CGC-ELF program in memory and prepares the initial CPU state
        and the stack.

        :param filename: pathname of the file to be executed.
        """
        CGC_MIN_PAGE_SIZE = 4096
        CGC_MIN_ALIGN = CGC_MIN_PAGE_SIZE
        TASK_SIZE = 0x80000000

        def CGC_PAGESTART(_v):
            return ((_v) & ~ (CGC_MIN_ALIGN - 1))

        def CGC_PAGEOFFSET(_v):
            return ((_v) & (CGC_MIN_ALIGN - 1))

        def CGC_PAGEALIGN(_v):
            return (((_v) + CGC_MIN_ALIGN - 1) & ~(CGC_MIN_ALIGN - 1))

        def BAD_ADDR(x):
            return ((x) >= TASK_SIZE)

        # load elf See https://github.com/CyberdyneNYC/linux-source-3.13.2-cgc/blob/master/fs/binfmt_cgc.c
        # read the ELF object file
        cgc = CGCElf(filename)
        logger.info("Loading %s as a %s elf" % (filename, cgc.arch))
        # make cpu and memory (Only 1 thread in Decree)
        cpu = self._mk_proc()

        bss = brk = 0
        start_code = 0xffffffff
        end_code = start_data = end_data = 0

        for (vaddr, memsz, perms, name, offset, filesz) in cgc.maps():
            if vaddr < start_code:
                start_code = vaddr
            if start_data < vaddr:
                start_data = vaddr

            if vaddr > TASK_SIZE or filesz > memsz or \
                    memsz > TASK_SIZE or TASK_SIZE - memsz < vaddr:
                raise Exception("Set_brk can never work. avoid overflows")

            # CGCMAP--
            addr = None
            if filesz > 0:
                hint = CGC_PAGESTART(vaddr)
                size = CGC_PAGEALIGN(filesz + CGC_PAGEOFFSET(vaddr))
                offset = CGC_PAGESTART(offset)
                addr = cpu.memory.mmapFile(hint, size, perms, name, offset)
                assert not BAD_ADDR(addr)

                lo = CGC_PAGEALIGN(vaddr + filesz)
                hi = CGC_PAGEALIGN(vaddr + memsz)
            else:
                # for 0 filesz, we have to include the first page as bss.
                lo = CGC_PAGESTART(vaddr + filesz)
                hi = CGC_PAGEALIGN(vaddr + memsz)

            # map anon pages for the rest (no prefault)
            if hi - lo > 0:
                zaddr = cpu.memory.mmap(lo, hi - lo, perms)
                assert not BAD_ADDR(zaddr)

            lo = vaddr + filesz
            hi = CGC_PAGEALIGN(vaddr + memsz)
            if hi - lo > 0:
                old_perms = cpu.memory.perms(lo)
                cpu.memory.mprotect(lo, hi - lo, 'rw')
                try:
                    cpu.memory[lo:hi] = '\x00' * (hi - lo)
                except Exception as e:
                    logger.debug("Exception zeroing main elf fractional pages: %s" % str(e))
                cpu.memory.mprotect(lo, hi, old_perms)

            if addr is None:
                addr = zaddr
            assert addr is not None

            k = vaddr + filesz
            if k > bss:
                bss = k
            if 'x' in perms and end_code < k:
                end_code = k
            if end_data < k:
                end_data = k

            k = vaddr + memsz
            if k > brk:
                brk = k

        bss = brk
        stack_base = 0xbaaaaffc
        stack_size = 0x800000
        stack = cpu.memory.mmap(0xbaaab000 - stack_size, stack_size, 'rwx') + stack_size - 4
        assert (stack_base) in cpu.memory and (stack_base - stack_size + 4) in cpu.memory

        # Only one thread in Decree
        status, thread = next(cgc.threads())
        assert status == 'Running'

        logger.info("Setting initial cpu state")
        # set initial CPU state
        cpu.write_register('EAX', 0x0)
        cpu.write_register('ECX', cpu.memory.mmap(CGC_PAGESTART(0x4347c000),
                                                  CGC_PAGEALIGN(4096 + CGC_PAGEOFFSET(0x4347c000)),
                                                  'rwx'))
        cpu.write_register('EDX', 0x0)
        cpu.write_register('EBX', 0x0)
        cpu.write_register('ESP', stack)
        cpu.write_register('EBP', 0x0)
        cpu.write_register('ESI', 0x0)
        cpu.write_register('EDI', 0x0)
        cpu.write_register('EIP', thread['EIP'])
        cpu.write_register('RFLAGS', 0x202)
        cpu.write_register('CS', 0x0)
        cpu.write_register('SS', 0x0)
        cpu.write_register('DS', 0x0)
        cpu.write_register('ES', 0x0)
        cpu.write_register('FS', 0x0)
        cpu.write_register('GS', 0x0)

        cpu.memory.mmap(0x4347c000, 0x1000, 'r')
        # cpu.memory[0x4347c000:0x4347d000] = 'A' 0x1000

        logger.info("Entry point: %016x", cpu.EIP)
        logger.info("Stack start: %016x", cpu.ESP)
        logger.info("Brk: %016x", brk)
        logger.info("Mappings:")
        for m in str(cpu.memory).split('\n'):
            logger.info("  %s", m)
        return [cpu]