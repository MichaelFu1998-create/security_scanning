def __run(self, shell=True, echo=True):
        """Run DMESG job"""

        if env():
            return 1

        cij.emph("cij.dmesg.start: shell: %r, cmd: %r" % (shell, self.__prefix + self.__suffix))

        return cij.ssh.command(self.__prefix, shell, echo, self.__suffix)