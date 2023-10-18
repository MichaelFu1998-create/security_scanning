def set_user_method(self, user_methods, forced=False):
        r'''Method to set the T, P, and composition dependent property methods 
        desired for consideration by the user. Can be used to exclude certain 
        methods which might have unacceptable accuracy.

        As a side effect, the previously selected method is removed when
        this method is called to ensure user methods are tried in the desired
        order.

        Parameters
        ----------
        user_methods : str or list
            Methods by name to be considered for calculation of the mixture
            property, ordered by preference.
        forced : bool, optional
            If True, only the user specified methods will ever be considered;
            if False, other methods will be considered if no user methods
            suceed.
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
            raise Exception("One of the given methods is not available for this mixture")
        if not self.user_methods and self.forced:
            raise Exception('Only user specified methods are considered when forced is True, but no methods were provided')

        # Remove previously selected methods
        self.method = None
        self.sorted_valid_methods = []
        self.TP_zs_ws_cached = (None, None, None, None)