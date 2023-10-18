def register(self, model, index_cls=AlgoliaIndex, auto_indexing=None):
        """
        Registers the given model with Algolia engine.

        If the given model is already registered with Algolia engine, a
        RegistrationError will be raised.
        """
        # Check for existing registration.
        if self.is_registered(model):
            raise RegistrationError(
                '{} is already registered with Algolia engine'.format(model))

        # Perform the registration.
        if not issubclass(index_cls, AlgoliaIndex):
            raise RegistrationError(
                '{} should be a subclass of AlgoliaIndex'.format(index_cls))
        index_obj = index_cls(model, self.client, self.__settings)
        self.__registered_models[model] = index_obj

        if (isinstance(auto_indexing, bool) and
                auto_indexing) or self.__auto_indexing:
            # Connect to the signalling framework.
            post_save.connect(self.__post_save_receiver, model)
            pre_delete.connect(self.__pre_delete_receiver, model)
            logger.info('REGISTER %s', model)