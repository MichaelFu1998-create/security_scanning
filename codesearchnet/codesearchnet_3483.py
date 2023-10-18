def sys_chroot(self, path):
        """
        An implementation of chroot that does perform some basic error checking,
        but does not actually chroot.

        :param path: Path to chroot
        """
        if path not in self.current.memory:
            return -errno.EFAULT

        path_s = self.current.read_string(path)
        if not os.path.exists(path_s):
            return -errno.ENOENT

        if not os.path.isdir(path_s):
            return -errno.ENOTDIR

        return -errno.EPERM