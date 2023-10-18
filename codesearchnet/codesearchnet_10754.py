def _fix_docs(this_abc, child_class):
        """Make api method docs inheritted.

        Specifically, insepect.getdoc will return values inheritted from this
        abc for standardized api methods.
        """
        # After python 3.5, this is basically handled automatically
        if sys.version_info >= (3, 5):
            return child_class

        if not issubclass(child_class, this_abc):
            raise KappaError('Cannot fix docs of class that is not decendent.')

        # This method is modified from solution given in
        # https://stackoverflow.com/a/8101598/8863865
        for name, child_func in vars(child_class).items():
            if callable(child_func) and not child_func.__doc__:
                if name in this_abc.__abstractmethods__:
                    parent_func = getattr(this_abc, name)
                    child_func.__doc__ = parent_func.__doc__
        return child_class