def get_3d_markers_no_label(
        self, component_info=None, data=None, component_position=None
    ):
        """Get 3D markers without label."""
        return self._get_3d_markers(
            RT3DMarkerPositionNoLabel, component_info, data, component_position
        )