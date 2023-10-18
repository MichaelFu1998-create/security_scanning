def fill(self, iterations=1):
        """Perform the gapfilling by iteratively solving the model, updating
        the costs and recording the used reactions.


        Parameters
        ----------
        iterations : int
            The number of rounds of gapfilling to perform. For every
            iteration, the penalty for every used reaction increases
            linearly. This way, the algorithm is encouraged to search for
            alternative solutions which may include previously used
            reactions. I.e., with enough iterations pathways including 10
            steps will eventually be reported even if the shortest pathway
            is a single reaction.

        Returns
        -------
        iterable
            A list of lists where each element is a list reactions that were
            used to gapfill the model.

        Raises
        ------
        RuntimeError
            If the model fails to be validated (i.e. the original model with
            the proposed reactions added, still cannot get the required flux
            through the objective).
        """
        used_reactions = list()
        for i in range(iterations):
            self.model.slim_optimize(error_value=None,
                                     message='gapfilling optimization failed')
            solution = [self.model.reactions.get_by_id(ind.rxn_id)
                        for ind in self.indicators if
                        ind._get_primal() > self.integer_threshold]
            if not self.validate(solution):
                raise RuntimeError('failed to validate gapfilled model, '
                                   'try lowering the integer_threshold')
            used_reactions.append(solution)
            self.update_costs()
        return used_reactions