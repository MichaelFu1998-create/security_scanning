def get_bbox(self, primitive):
        """Get the bounding box for the mesh"""
        accessor = primitive.attributes.get('POSITION')
        return accessor.min, accessor.max