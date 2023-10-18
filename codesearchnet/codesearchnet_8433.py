def terminate(self):
        """Terminate DMESG job"""

        if self.__thread:
            cmd = ["who am i"]
            status, output, _ = cij.util.execute(cmd, shell=True, echo=True)
            if status:
                cij.warn("cij.dmesg.terminate: who am i failed")
                return 1

            tty = output.split()[1]

            cmd = ["pkill -f '{}' -t '{}'".format(" ".join(self.__prefix), tty)]
            status, _, _ = cij.util.execute(cmd, shell=True, echo=True)
            if status:
                cij.warn("cij.dmesg.terminate: pkill failed")
                return 1

            self.__thread.join()
            self.__thread = None

        return 0