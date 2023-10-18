def delete(self, force=False, **kwargs):
        """
        It is impossible to delete an activatable model unless force is True. This function instead sets it to inactive.
        """
        if force:
            return super(BaseActivatableModel, self).delete(**kwargs)
        else:
            setattr(self, self.ACTIVATABLE_FIELD_NAME, False)
            return self.save(update_fields=[self.ACTIVATABLE_FIELD_NAME])