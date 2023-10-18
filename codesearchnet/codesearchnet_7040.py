def select_valid_methods_P(self, T, P):
        r'''Method to obtain a sorted list methods which are valid at `T`
        according to `test_method_validity`. Considers either only user methods
        if forced is True, or all methods. User methods are first tested
        according to their listed order, and unless forced is True, then all
        methods are tested and sorted by their order in `ranked_methods`.

        Parameters
        ----------
        T : float
            Temperature at which to test methods, [K]
        P : float
            Pressure at which to test methods, [Pa]

        Returns
        -------
        sorted_valid_methods_P : list
            Sorted lists of methods valid at T and P according to
            `test_method_validity`
        '''
        # Same as select_valid_methods but with _P added to variables
        if self.forced_P:
            considered_methods = list(self.user_methods_P)
        else:
            considered_methods = list(self.all_methods_P)

        if self.user_methods_P:
            [considered_methods.remove(i) for i in self.user_methods_P]

        preferences = sorted([self.ranked_methods_P.index(i) for i in considered_methods])
        sorted_methods = [self.ranked_methods_P[i] for i in preferences]

        if self.user_methods_P:
            [sorted_methods.insert(0, i) for i in reversed(self.user_methods_P)]

        sorted_valid_methods_P = []
        for method in sorted_methods:
            if self.test_method_validity_P(T, P, method):
                sorted_valid_methods_P.append(method)

        return sorted_valid_methods_P