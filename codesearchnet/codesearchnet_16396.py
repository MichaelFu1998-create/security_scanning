def get_3d_markers(self, component_info=None, data=None, component_position=None):
        """Get 3D markers."""
        return self._get_3d_markers(
            RT3DMarkerPosition, component_info, data, component_position
        )