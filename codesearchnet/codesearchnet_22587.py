def handle_rereduce(self, reduce_function_names, values):
        """Re-reduce a set of values, with a list of rereduction functions."""
        # This gets a large list of reduction functions, given their names.
        reduce_functions = []
        for reduce_function_name in reduce_function_names:
            try:
                reduce_function = get_function(reduce_function_name)
                if getattr(reduce_function, 'view_decorated', None):
                    reduce_function = reduce_function(self.log)
                reduce_functions.append(reduce_function)
            except Exception, exc:
                self.log(repr(exc))
                reduce_functions.append(lambda *args, **kwargs: None)
        # This gets the list of results from those functions.
        results = []
        for reduce_function in reduce_functions:
            try:
                results.append(reduce_function(None, values, rereduce=True))
            except Exception, exc:
                self.log(repr(exc))
                results.append(None)
        return [True, results]