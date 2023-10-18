def add_path_object(self, *args):
        """
        Add custom path objects

        :type: path_object: static_bundle.paths.AbstractPath
        """
        for obj in args:
            obj.bundle = self
            self.files.append(obj)