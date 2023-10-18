def get_3d_markers_no_label_residual(
        self, component_info=None, data=None, component_position=None
    ):
        """Get 3D markers without label with residual."""
        return self._get_3d_markers(
            RT3DMarkerPositionNoLabelResidual, component_info, data, component_position
        )