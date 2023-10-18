def _is_ndb(self):
        """Determine whether the model of the instance is an NDB model.

        Returns:
            Boolean indicating whether or not the model is an NDB or DB model.
        """
        # issubclass will fail if one of the arguments is not a class, only
        # need worry about new-style classes since ndb and db models are
        # new-style
        if isinstance(self._model, type):
            if _NDB_MODEL is not None and issubclass(self._model, _NDB_MODEL):
                return True
            elif issubclass(self._model, db.Model):
                return False

        raise TypeError(
            'Model class not an NDB or DB model: {0}.'.format(self._model))