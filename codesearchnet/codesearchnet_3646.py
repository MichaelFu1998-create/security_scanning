def add_finding(self, state, address, pc, finding, at_init, constraint=True):
        """
        Logs a finding at specified contract and assembler line.
        :param state: current state
        :param address: contract address of the finding
        :param pc: program counter of the finding
        :param at_init: true if executing the constructor
        :param finding: textual description of the finding
        :param constraint: finding is considered reproducible only when constraint is True
        """

        if issymbolic(pc):
            pc = simplify(pc)
        if isinstance(pc, Constant):
            pc = pc.value
        if not isinstance(pc, int):
            raise ValueError("PC must be a number")
        self.get_findings(state).add((address, pc, finding, at_init, constraint))
        with self.locked_global_findings() as gf:
            gf.add((address, pc, finding, at_init))
        #Fixme for ever broken logger
        logger.warning(finding)