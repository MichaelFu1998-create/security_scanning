def unregister(self, model):
        """
        Unregisters the given model with Algolia engine.

        If the given model is not registered with Algolia engine, a
        RegistrationError will be raised.
        """
        if not self.is_registered(model):
            raise RegistrationError(
                '{} is not registered with Algolia engine'.format(model))
        # Perform the unregistration.
        del self.__registered_models[model]

        # Disconnect from the signalling framework.
        post_save.disconnect(self.__post_save_receiver, model)
        pre_delete.disconnect(self.__pre_delete_receiver, model)
        logger.info('UNREGISTER %s', model)