def load_gltf(self):
        """Loads a gltf json file"""
        with open(self.path) as fd:
            self.meta = GLTFMeta(self.path, json.load(fd))