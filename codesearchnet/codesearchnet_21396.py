def count(self, *args, **kwargs):
        """
            Returns the number of results after filtering with the given arguments.
        """
        search = self.create_search(*args, **kwargs)
        try:
            return search.count()
        except NotFoundError:
            print_error("The index was not found, have you initialized the index?")
        except (ConnectionError, TransportError):
            print_error("Cannot connect to elasticsearch")