def _in_user_func(state):
        """
        :param state: current state
        :return: whether the current execution is in a user-defined function or not.

        NOTE / TODO / FIXME: As this may produce false postives, this is not in the base `Detector` class.
        It should be fixed at some point and moved there. See below.

        The first 4 bytes of tx data is keccak256 hash of the function signature that is called by given tx.

        All transactions start within Solidity dispatcher function: it takes passed hash and dispatches
        the execution to given function based on it.

        So: if we are in the dispatcher, *and contract have some functions* one of the first four tx data bytes
        will effectively have more than one solutions.

        BUT if contract have only a fallback function, the equation below may return more solutions when we are
        in a dispatcher function.  <--- because of that, we warn that the detector is not that stable
        for contracts with only a fallback function.
        """

        # If we are already in user function (we cached it) let's just return True
        in_function = state.context.get('in_function', False)
        prev_tx_count = state.context.get('prev_tx_count', 0)
        curr_tx_count = len(state.platform.transactions)

        new_human_tx = prev_tx_count != curr_tx_count

        if in_function and not new_human_tx:
            return True

        # This is expensive call, so we cache it
        in_function = len(state.solve_n(state.platform.current_transaction.data[:4], 2)) == 1

        state.context['in_function'] = in_function
        state.context['prev_tx_count'] = curr_tx_count

        return in_function