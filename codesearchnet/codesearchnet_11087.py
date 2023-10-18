def load(self):
        """
        Loads this project instance
        """
        self.create_effect_classes()

        self._add_resource_descriptions_to_pools(self.create_external_resources())
        self._add_resource_descriptions_to_pools(self.create_resources())

        for meta, resource in resources.textures.load_pool():
            self._textures[meta.label] = resource

        for meta, resource in resources.programs.load_pool():
            self._programs[meta.label] = resource

        for meta, resource in resources.scenes.load_pool():
            self._scenes[meta.label] = resource

        for meta, resource in resources.data.load_pool():
            self._data[meta.label] = resource

        self.create_effect_instances()
        self.post_load()