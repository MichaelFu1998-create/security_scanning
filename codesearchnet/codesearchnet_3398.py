def _visited_callback(self, state, pc, instr):
        """ Maintain our own copy of the visited set
        """
        pc = state.platform.current.PC
        with self.locked_context('visited', dict) as ctx:
            ctx[pc] = ctx.get(pc, 0) + 1