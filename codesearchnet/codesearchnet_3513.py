def sys_terminate(self, cpu, error_code):
        """
        Exits all threads in a process
        :param cpu: current CPU.
        :raises Exception: 'Finished'
        """
        procid = self.procs.index(cpu)
        self.sched()
        self.running.remove(procid)
        # self.procs[procid] = None #let it there so we can report?
        if issymbolic(error_code):
            logger.info("TERMINATE PROC_%02d with symbolic exit code [%d,%d]", procid, solver.minmax(self.constraints, error_code))
        else:
            logger.info("TERMINATE PROC_%02d %x", procid, error_code)
        if len(self.running) == 0:
            raise TerminateState(f'Process exited correctly. Code: {error_code}')
        return error_code