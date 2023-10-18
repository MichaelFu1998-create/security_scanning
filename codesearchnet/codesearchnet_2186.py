def save_component(self, component_name, save_path):
        """
        Saves a component of this model to the designated location.

        Args:
            component_name: The component to save.
            save_path: The location to save to.
        Returns:
            Checkpoint path where the component was saved.
        """
        component = self.get_component(component_name=component_name)
        self._validate_savable(component=component, component_name=component_name)
        return component.save(sess=self.session, save_path=save_path)