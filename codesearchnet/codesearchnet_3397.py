def _visited_callback(self, state, pc, instr):
        """ Maintain our own copy of the visited set
        """
        with self.locked_context('visited', set) as ctx:
            ctx.add(pc)