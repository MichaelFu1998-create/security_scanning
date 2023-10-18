def sys_arch_prctl(self, code, addr):
        """
        Sets architecture-specific thread state
        :rtype: int

        :param code: must be C{ARCH_SET_FS}.
        :param addr: the base address of the FS segment.
        :return: C{0} on success
        :raises error:
            - if C{code} is different to C{ARCH_SET_FS}
        """
        ARCH_SET_GS = 0x1001
        ARCH_SET_FS = 0x1002
        ARCH_GET_FS = 0x1003
        ARCH_GET_GS = 0x1004
        if code not in {ARCH_SET_GS, ARCH_SET_FS, ARCH_GET_FS, ARCH_GET_GS}:
            logger.debug("code not in expected options ARCH_GET/SET_FS/GS")
            return -errno.EINVAL
        if code != ARCH_SET_FS:
            raise NotImplementedError("Manticore supports only arch_prctl with code=ARCH_SET_FS (0x1002) for now")
        self.current.FS = 0x63
        self.current.set_descriptor(self.current.FS, addr, 0x4000, 'rw')
        return 0