def _should_really_index(self, instance):
        """Return True if according to should_index the object should be indexed."""
        if self._should_index_is_method:
            is_method = inspect.ismethod(self.should_index)
            try:
                count_args = len(inspect.signature(self.should_index).parameters)
            except AttributeError:
                # noinspection PyDeprecation
                count_args = len(inspect.getargspec(self.should_index).args)

            if is_method or count_args is 1:
                # bound method, call with instance
                return self.should_index(instance)
            else:
                # unbound method, simply call without arguments
                return self.should_index()
        else:
            # property/attribute/Field, evaluate as bool
            attr_type = type(self.should_index)
            if attr_type is DeferredAttribute:
                attr_value = self.should_index.__get__(instance, None)
            elif attr_type is str:
                attr_value = getattr(instance, self.should_index)
            elif attr_type is property:
                attr_value = self.should_index.__get__(instance)
            else:
                raise AlgoliaIndexError('{} should be a boolean attribute or a method that returns a boolean.'.format(
                    self.should_index))
            if type(attr_value) is not bool:
                raise AlgoliaIndexError("%s's should_index (%s) should be a boolean" % (
                    instance.__class__.__name__, self.should_index))
            return attr_value