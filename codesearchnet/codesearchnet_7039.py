def set_user_methods_P(self, user_methods_P, forced_P=False):
        r'''Method to set the pressure-dependent property methods desired for
        consideration by the user. Can be used to exclude certain methods which
        might have unacceptable accuracy.

        As a side effect, the previously selected method is removed when
        this method is called to ensure user methods are tried in the desired
        order.

        Parameters
        ----------
        user_methods_P : str or list
            Methods by name to be considered or preferred for pressure effect.
        forced : bool, optional
            If True, only the user specified methods will ever be considered;
            if False other methods will be considered if no user methods
            suceed.
        '''
        # Accept either a string or a list of methods, and whether
        # or not to only consider the false methods
        if isinstance(user_methods_P, str):
            user_methods_P = [user_methods_P]

        # The user's order matters and is retained for use by select_valid_methods
        self.user_methods_P = user_methods_P
        self.forced_P = forced_P

        # Validate that the user's specified methods are actual methods
        if set(self.user_methods_P).difference(self.all_methods_P):
            raise Exception("One of the given methods is not available for this chemical")
        if not self.user_methods_P and self.forced:
            raise Exception('Only user specified methods are considered when forced is True, but no methods were provided')

        # Remove previously selected methods
        self.method_P = None
        self.sorted_valid_methods_P = []
        self.TP_cached = None