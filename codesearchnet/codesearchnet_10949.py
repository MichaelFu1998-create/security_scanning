def check_extensions(self, supported):
        """
        "extensionsRequired": ["KHR_draco_mesh_compression"],
        "extensionsUsed": ["KHR_draco_mesh_compression"]
        """
        if self.data.get('extensionsRequired'):
            for ext in self.data.get('extensionsRequired'):
                if ext not in supported:
                    raise ValueError("Extension {} not supported".format(ext))

        if self.data.get('extensionsUsed'):
            for ext in self.data.get('extensionsUsed'):
                if ext not in supported:
                    raise ValueError("Extension {} not supported".format(ext))