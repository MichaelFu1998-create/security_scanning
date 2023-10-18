def handle_reduce(self, reduce_function_names, mapped_docs):
        """Reduce several mapped documents by several reduction functions."""
        reduce_functions = []
        # This gets a large list of reduction functions, given their names.
        for reduce_function_name in reduce_function_names:
            try:
                reduce_function = get_function(reduce_function_name)
                if getattr(reduce_function, 'view_decorated', None):
                    reduce_function = reduce_function(self.log)
                reduce_functions.append(reduce_function)
            except Exception, exc:
                self.log(repr(exc))
                reduce_functions.append(lambda *args, **kwargs: None)
        # Transform lots of (key, value) pairs into one (keys, values) pair.
        keys, values = zip(
            (key, value) for ((key, doc_id), value) in mapped_docs)
        # This gets the list of results from the reduction functions.
        results = []
        for reduce_function in reduce_functions:
            try:
                results.append(reduce_function(keys, values, rereduce=False))
            except Exception, exc:
                self.log(repr(exc))
                results.append(None)
        return [True, results]