def commandline(self, **mpiargs):
        """Returns simple command line to invoke mdrun.

        If :attr:`mpiexec` is set then :meth:`mpicommand` provides the mpi
        launcher command that prefixes the actual ``mdrun`` invocation:

           :attr:`mpiexec` [*mpiargs*]  :attr:`mdrun` [*mdrun-args*]

        The *mdrun-args* are set on initializing the class. Override
        :meth:`mpicommand` to fit your system if the simple default
        OpenMP launcher is not appropriate.
        """
        cmd = self.MDRUN.commandline()
        if self.mpiexec:
            cmd = self.mpicommand(**mpiargs) + cmd
        return cmd