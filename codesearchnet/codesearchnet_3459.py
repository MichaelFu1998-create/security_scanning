def empty_platform(cls, arch):
        """
        Create a platform without an ELF loaded.

        :param str arch: The architecture of the new platform
        :rtype: Linux
        """
        platform = cls(None)
        platform._init_cpu(arch)
        platform._init_std_fds()
        return platform