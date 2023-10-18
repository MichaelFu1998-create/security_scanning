def _save_current_location(self, state, finding, condition=True):
        """
        Save current location in the internal locations list and returns a textual id for it.
        This is used to save locations that could later be promoted to a finding if other conditions hold
        See _get_location()
        :param state: current state
        :param finding: textual description of the finding
        :param condition: general purpose constraint
        """
        address = state.platform.current_vm.address
        pc = state.platform.current_vm.pc
        at_init = state.platform.current_transaction.sort == 'CREATE'
        location = (address, pc, finding, at_init, condition)
        hash_id = hashlib.sha1(str(location).encode()).hexdigest()
        state.context.setdefault('{:s}.locations'.format(self.name), {})[hash_id] = location
        return hash_id