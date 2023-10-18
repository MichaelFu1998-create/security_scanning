def save(self, *args, **kwargs):
        """
        A custom save method that handles figuring out when something is activated or deactivated.
        """
        current_activable_value = getattr(self, self.ACTIVATABLE_FIELD_NAME)
        is_active_changed = self.id is None or self.__original_activatable_value != current_activable_value
        self.__original_activatable_value = current_activable_value

        ret_val = super(BaseActivatableModel, self).save(*args, **kwargs)

        # Emit the signals for when the is_active flag is changed
        if is_active_changed:
            model_activations_changed.send(self.__class__, instance_ids=[self.id], is_active=current_activable_value)
        if self.activatable_field_updated:
            model_activations_updated.send(self.__class__, instance_ids=[self.id], is_active=current_activable_value)

        return ret_val