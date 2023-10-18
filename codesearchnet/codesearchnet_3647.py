def add_finding_here(self, state, finding, constraint=True):
        """
        Logs a finding in current contract and assembler line.
        :param state: current state
        :param finding: textual description of the finding
        :param constraint: finding is considered reproducible only when constraint is True
        """
        address = state.platform.current_vm.address
        pc = state.platform.current_vm.pc
        if isinstance(pc, Constant):
            pc = pc.value
        if not isinstance(pc, int):
            raise ValueError("PC must be a number")
        at_init = state.platform.current_transaction.sort == 'CREATE'
        self.add_finding(state, address, pc, finding, at_init, constraint)