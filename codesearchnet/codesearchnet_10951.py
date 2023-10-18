def load_indices(self, primitive):
        """Loads the index buffer / polygon list for a primitive"""
        if getattr(primitive, "indices") is None:
            return None, None

        _, component_type, buffer = primitive.indices.read()
        return component_type, buffer