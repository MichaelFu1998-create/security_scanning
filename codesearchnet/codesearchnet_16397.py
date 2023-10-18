def get_3d_markers_residual(
        self, component_info=None, data=None, component_position=None
    ):
        """Get 3D markers with residual."""
        return self._get_3d_markers(
            RT3DMarkerPositionResidual, component_info, data, component_position
        )