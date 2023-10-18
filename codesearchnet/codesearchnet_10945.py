def load(self):
        """
        Deferred loading of the scene

        :param scene: The scene object
        :param file: Resolved path if changed by finder
        """
        self.path = self.find_scene(self.meta.path)
        if not self.path:
            raise ValueError("Scene '{}' not found".format(self.meta.path))

        self.scene = Scene(self.path)

        # Load gltf json file
        if self.path.suffix == '.gltf':
            self.load_gltf()

        # Load binary gltf file
        if self.path.suffix == '.glb':
            self.load_glb()

        self.meta.check_version()
        self.meta.check_extensions(self.supported_extensions)
        self.load_images()
        self.load_samplers()
        self.load_textures()
        self.load_materials()
        self.load_meshes()
        self.load_nodes()

        self.scene.calc_scene_bbox()
        self.scene.prepare()

        return self.scene