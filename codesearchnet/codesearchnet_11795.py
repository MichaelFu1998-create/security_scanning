def register(self):
        """
        Adds this satchel to the global registeries for fast lookup from other satchels.
        """

        self._set_defaults()

        all_satchels[self.name.upper()] = self

        manifest_recorder[self.name] = self.record_manifest

        # Register service commands.
        if self.required_system_packages:
            required_system_packages[self.name.upper()] = self.required_system_packages