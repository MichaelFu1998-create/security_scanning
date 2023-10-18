def _create(cls, model_class, *args, **kwargs):
        """
        Create a new user instance.

        Args:
            model_class:
                The type of model to create an instance of.
            args:
                Positional arguments to create the instance with.
            kwargs:
                Keyword arguments to create the instance with.

        Returns:
            A new user instance of the type specified by
            ``model_class``.
        """
        manager = cls._get_manager(model_class)

        return manager.create_user(*args, **kwargs)