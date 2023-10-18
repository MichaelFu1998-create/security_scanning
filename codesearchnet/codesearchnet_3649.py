def _get_location(self, state, hash_id):
        """
        Get previously saved location
        A location is composed of: address, pc, finding, at_init, condition
        """
        return state.context.setdefault('{:s}.locations'.format(self.name), {})[hash_id]