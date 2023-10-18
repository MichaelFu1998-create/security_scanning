def select_valid_methods(self, T):
        r'''Method to obtain a sorted list of methods which are valid at `T`
        according to `test_method_validity`. Considers either only user methods
        if forced is True, or all methods. User methods are first tested
        according to their listed order, and unless forced is True, then all
        methods are tested and sorted by their order in `ranked_methods`.

        Parameters
        ----------
        T : float
            Temperature at which to test methods, [K]

        Returns
        -------
        sorted_valid_methods : list
            Sorted lists of methods valid at T according to
            `test_method_validity`
        '''
        # Consider either only the user's methods or all methods
        # Tabular data will be in both when inserted
        if self.forced:
            considered_methods = list(self.user_methods)
        else:
            considered_methods = list(self.all_methods)

        # User methods (incl. tabular data); add back later, after ranking the rest
        if self.user_methods:
            [considered_methods.remove(i) for i in self.user_methods]

        # Index the rest of the methods by ranked_methods, and add them to a list, sorted_methods
        preferences = sorted([self.ranked_methods.index(i) for i in considered_methods])
        sorted_methods = [self.ranked_methods[i] for i in preferences]

        # Add back the user's methods to the top, in order.
        if self.user_methods:
            [sorted_methods.insert(0, i) for i in reversed(self.user_methods)]

        sorted_valid_methods = []
        for method in sorted_methods:
            if self.test_method_validity(T, method):
                sorted_valid_methods.append(method)

        return sorted_valid_methods