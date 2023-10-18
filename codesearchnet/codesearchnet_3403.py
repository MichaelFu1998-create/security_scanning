def fork(self, state, expression, policy='ALL', setstate=None):
        """
        Fork state on expression concretizations.
        Using policy build a list of solutions for expression.
        For the state on each solution setting the new state with setstate

        For example if expression is a Bool it may have 2 solutions. True or False.

                                 Parent
                            (expression = ??)

                   Child1                         Child2
            (expression = True)             (expression = True)
               setstate(True)                   setstate(False)

        The optional setstate() function is supposed to set the concrete value
        in the child state.

        """
        assert isinstance(expression, Expression)

        if setstate is None:
            setstate = lambda x, y: None

        # Find a set of solutions for expression
        solutions = state.concretize(expression, policy)

        if not solutions:
            raise ExecutorError("Forking on unfeasible constraint set")

        if len(solutions) == 1:
            setstate(state, solutions[0])
            return state

        logger.info("Forking. Policy: %s. Values: %s",
                    policy,
                    ', '.join(f'0x{sol:x}' for sol in solutions))

        self._publish('will_fork_state', state, expression, solutions, policy)

        # Build and enqueue a state for each solution
        children = []
        for new_value in solutions:
            with state as new_state:
                new_state.constrain(expression == new_value)

                # and set the PC of the new state to the concrete pc-dest
                #(or other register or memory address to concrete)
                setstate(new_state, new_value)

                self._publish('did_fork_state', new_state, expression, new_value, policy)

                # enqueue new_state
                state_id = self.enqueue(new_state)
                # maintain a list of children for logging purpose
                children.append(state_id)

        logger.info("Forking current state into states %r", children)
        return None