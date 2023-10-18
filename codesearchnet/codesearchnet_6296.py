def remove_groups(self, group_list):
        """Remove groups from the model.

        Members of each group are not removed
        from the model (i.e. metabolites, reactions, and genes in the group
        stay in the model after any groups containing them are removed).

        Parameters
        ----------
        group_list : list
            A list of `cobra.Group` objects to remove from the model.
        """

        if isinstance(group_list, string_types) or \
                hasattr(group_list, "id"):
            warn("need to pass in a list")
            group_list = [group_list]

        for group in group_list:
            # make sure the group is in the model
            if group.id not in self.groups:
                LOGGER.warning("%r not in %r. Ignored.", group, self)
            else:
                self.groups.remove(group)
                group._model = None