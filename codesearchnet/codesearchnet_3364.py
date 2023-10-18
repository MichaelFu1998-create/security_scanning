def _is_sat(self) -> bool:
        """
        Check the satisfiability of the current state

        :return: whether current state is satisfiable or not.
        """
        logger.debug("Solver.check() ")
        start = time.time()
        self._send('(check-sat)')
        status = self._recv()
        logger.debug("Check took %s seconds (%s)", time.time() - start, status)
        if status not in ('sat', 'unsat', 'unknown'):
            raise SolverError(status)
        if consider_unknown_as_unsat:
            if status == 'unknown':
                logger.info('Found an unknown core, probably a solver timeout')
                status = 'unsat'

        if status == 'unknown':
            raise SolverUnknown(status)

        return status == 'sat'