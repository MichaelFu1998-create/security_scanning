def merge_from_list(self, list_args):
        """find any matching parser_args from list_args and merge them into this
        instance

        list_args -- list -- an array of (args, kwargs) tuples
        """
        def xs(name, parser_args, list_args):
            """build the generator of matching list_args"""
            for args, kwargs in list_args:
                if len(set(args) & parser_args) > 0:
                    yield args, kwargs

                else:
                    if 'dest' in kwargs:
                        if kwargs['dest'] == name:
                            yield args, kwargs

        for args, kwargs in xs(self.name, self.parser_args, list_args):
            self.merge_args(args)
            self.merge_kwargs(kwargs)