def add(self, constraint, check=False):
        """
        Add a constraint to the set

        :param constraint: The constraint to add to the set.
        :param check: Currently unused.
        :return:
        """
        if isinstance(constraint, bool):
            constraint = BoolConstant(constraint)
        assert isinstance(constraint, Bool)
        constraint = simplify(constraint)
        # If self._child is not None this constraint set has been forked and a
        # a derived constraintset may be using this. So we can't add any more
        # constraints to this one. After the child constraintSet is deleted
        # we regain the ability to add constraints.
        if self._child is not None:
            raise Exception('ConstraintSet is frozen')

        if isinstance(constraint, BoolConstant):
            if not constraint.value:
                logger.info("Adding an impossible constant constraint")
                self._constraints = [constraint]
            else:
                return

        self._constraints.append(constraint)

        if check:
            from ...core.smtlib import solver
            if not solver.check(self):
                raise ValueError("Added an impossible constraint")