def get_adapter(self, model):
        """Returns the adapter associated with the given model."""
        if not self.is_registered(model):
            raise RegistrationError(
                '{} is not registered with Algolia engine'.format(model))

        return self.__registered_models[model]