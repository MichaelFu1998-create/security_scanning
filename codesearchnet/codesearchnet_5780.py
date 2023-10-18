def _delete_entity(self):
        """Delete entity from datastore.

        Attempts to delete using the key_name stored on the object, whether or
        not the given key is in the datastore.
        """
        if self._is_ndb():
            _NDB_KEY(self._model, self._key_name).delete()
        else:
            entity_key = db.Key.from_path(self._model.kind(), self._key_name)
            db.delete(entity_key)