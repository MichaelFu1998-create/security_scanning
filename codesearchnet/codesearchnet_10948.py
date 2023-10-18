def _link_data(self):
        """Add references"""
        # accessors -> buffer_views -> buffers
        for acc in self.accessors:
            acc.bufferView = self.buffer_views[acc.bufferViewId]

        for buffer_view in self.buffer_views:
            buffer_view.buffer = self.buffers[buffer_view.bufferId]

        # Link accessors to mesh primitives
        for mesh in self.meshes:
            for primitive in mesh.primitives:
                if getattr(primitive, "indices", None) is not None:
                    primitive.indices = self.accessors[primitive.indices]
                for name, value in primitive.attributes.items():
                    primitive.attributes[name] = self.accessors[value]

        # Link buffer views to images
        for image in self.images:
            if image.bufferViewId is not None:
                image.bufferView = self.buffer_views[image.bufferViewId]