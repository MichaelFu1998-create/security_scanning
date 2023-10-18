def add_groups(self, group_list):
        """Add groups to the model.

        Groups with identifiers identical to a group already in the model are
        ignored.

        If any group contains members that are not in the model, these members
        are added to the model as well. Only metabolites, reactions, and genes
        can have groups.

        Parameters
        ----------
        group_list : list
            A list of `cobra.Group` objects to add to the model.
        """

        def existing_filter(group):
            if group.id in self.groups:
                LOGGER.warning(
                    "Ignoring group '%s' since it already exists.", group.id)
                return False
            return True

        if isinstance(group_list, string_types) or \
                hasattr(group_list, "id"):
            warn("need to pass in a list")
            group_list = [group_list]

        pruned = DictList(filter(existing_filter, group_list))

        for group in pruned:
            group._model = self
            for member in group.members:
                # If the member is not associated with the model, add it
                if isinstance(member, Metabolite):
                    if member not in self.metabolites:
                        self.add_metabolites([member])
                if isinstance(member, Reaction):
                    if member not in self.reactions:
                        self.add_reactions([member])
                # TODO(midnighter): `add_genes` method does not exist.
                # if isinstance(member, Gene):
                #     if member not in self.genes:
                #         self.add_genes([member])

            self.groups += [group]