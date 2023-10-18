def set_user_methods(self, user_methods, forced=False):
        r'''Method used to select certain property methods as having a higher
        priority than were set by default. If `forced` is true, then methods
        which were not specified are excluded from consideration.

        As a side effect, `method` is removed to ensure than the new methods
        will be used in calculations afterwards.

        An exception is raised if any of the methods specified aren't available
        for the chemical. An exception is raised if no methods are provided.

        Parameters
        ----------
        user_methods : str or list
            Methods by name to be considered or prefered
        forced : bool, optional
            If True, only the user specified methods will ever be considered;
            if False other methods will be considered if no user methods
            suceed
        '''
        # Accept either a string or a list of methods, and whether
        # or not to only consider the false methods
        if isinstance(user_methods, str):
            user_methods = [user_methods]

        # The user's order matters and is retained for use by select_valid_methods
        self.user_methods = user_methods
        self.forced = forced

        # Validate that the user's specified methods are actual methods
        if set(self.user_methods).difference(self.all_methods):
            raise Exception("One of the given methods is not available for this chemical")
        if not self.user_methods and self.forced:
            raise Exception('Only user specified methods are considered when forced is True, but no methods were provided')

        # Remove previously selected methods
        self.method = None
        self.sorted_valid_methods = []
        self.T_cached = None