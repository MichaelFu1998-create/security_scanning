def run(self, shell=True, cmdline=False, echo=True):
        """Run FIO job"""

        if env():
            return 1

        cmd = ["fio"] + self.__parse_parms()
        if cmdline:
            cij.emph("cij.fio.run: shell: %r, cmd: %r" % (shell, cmd))

        return cij.ssh.command(cmd, shell, echo)