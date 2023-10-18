def merge_kwargs(self, kwargs):
        """these kwargs come from the @arg decorator, they are then merged into any
        keyword arguments that were automatically generated from the main function
        introspection"""
        if kwargs:
            self.parser_kwargs.update(kwargs)

        #self.parser_kwargs['dest'] = self.name
        self.parser_kwargs.setdefault('dest', self.name)

        # special handling of any passed in values
        if 'default' in kwargs:
            # NOTE -- this doesn't use .set_default() because that is meant to
            # parse from the function definition so it actually has different syntax
            # than what the .set_default() method does. eg, @arg("--foo", default=[1, 2]) means
            # that the default value should be an array with 1 and 2 in it, where main(foo=[1, 2])
            # means foo should be constrained to choices=[1, 2]
            self.parser_kwargs["default"] = kwargs["default"]
            self.parser_kwargs["required"] = False

        elif 'action' in kwargs:
            if kwargs['action'] in set(['store_false', 'store_true']):
                self.parser_kwargs['required'] = False

            elif kwargs['action'] in set(['version']):
                self.parser_kwargs.pop('required', False)

        else:
            self.parser_kwargs.setdefault("required", True)