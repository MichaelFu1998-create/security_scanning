def handle_map_doc(self, document):
        """Return the mapping of a document according to the function list."""
        # This uses the stored set of functions, sorted by order of addition.
        for function in sorted(self.functions.values(), key=lambda x: x[0]):
            try:
                # It has to be run through ``list``, because it may be a
                # generator function.
                yield [list(function(document))]
            except Exception, exc:
                # Otherwise, return an empty list and log the event.
                yield []
                self.log(repr(exc))