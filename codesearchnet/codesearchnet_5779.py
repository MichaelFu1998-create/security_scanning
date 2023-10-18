def _get_entity(self):
        """Retrieve entity from datastore.

        Uses a different model method for db or ndb models.

        Returns:
            Instance of the model corresponding to the current storage object
            and stored using the key name of the storage object.
        """
        if self._is_ndb():
            return self._model.get_by_id(self._key_name)
        else:
            return self._model.get_by_key_name(self._key_name)