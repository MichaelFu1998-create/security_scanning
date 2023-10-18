def restore_component(self, component_name, save_path):
        """
        Restores a component's parameters from a save location.

        Args:
            component_name: The component to restore.
            save_path: The save location.
        """
        component = self.get_component(component_name=component_name)
        self._validate_savable(component=component, component_name=component_name)
        component.restore(sess=self.session, save_path=save_path)