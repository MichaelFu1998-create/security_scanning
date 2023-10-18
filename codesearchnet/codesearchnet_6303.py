def merge(self, right, prefix_existing=None, inplace=True,
              objective='left'):
        """Merge two models to create a model with the reactions from both
        models.

        Custom constraints and variables from right models are also copied
        to left model, however note that, constraints and variables are
        assumed to be the same if they have the same name.

        right : cobra.Model
            The model to add reactions from
        prefix_existing : string
            Prefix the reaction identifier in the right that already exist
            in the left model with this string.
        inplace : bool
            Add reactions from right directly to left model object.
            Otherwise, create a new model leaving the left model untouched.
            When done within the model as context, changes to the models are
            reverted upon exit.
        objective : string
            One of 'left', 'right' or 'sum' for setting the objective of the
            resulting model to that of the corresponding model or the sum of
            both.
        """
        if inplace:
            new_model = self
        else:
            new_model = self.copy()
            new_model.id = '{}_{}'.format(self.id, right.id)
        new_reactions = deepcopy(right.reactions)
        if prefix_existing is not None:
            existing = new_reactions.query(
                lambda rxn: rxn.id in self.reactions)
            for reaction in existing:
                reaction.id = '{}{}'.format(prefix_existing, reaction.id)
        new_model.add_reactions(new_reactions)
        interface = new_model.problem
        new_vars = [interface.Variable.clone(v) for v in right.variables if
                    v.name not in new_model.variables]
        new_model.add_cons_vars(new_vars)
        new_cons = [interface.Constraint.clone(c, model=new_model.solver)
                    for c in right.constraints if
                    c.name not in new_model.constraints]
        new_model.add_cons_vars(new_cons, sloppy=True)
        new_model.objective = dict(
            left=self.objective,
            right=right.objective,
            sum=self.objective.expression + right.objective.expression
        )[objective]
        return new_model