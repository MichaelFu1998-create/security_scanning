def get_6d_euler(self, component_info=None, data=None, component_position=None):
        """Get 6D data with euler rotations."""
        components = []
        append_components = components.append
        for _ in range(component_info.body_count):
            component_position, position = QRTPacket._get_exact(
                RT6DBodyPosition, data, component_position
            )
            component_position, euler = QRTPacket._get_exact(
                RT6DBodyEuler, data, component_position
            )
            append_components((position, euler))
        return components