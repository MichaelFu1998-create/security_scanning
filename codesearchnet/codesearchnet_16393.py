def get_6d(self, component_info=None, data=None, component_position=None):
        """Get 6D data."""
        components = []
        append_components = components.append
        for _ in range(component_info.body_count):
            component_position, position = QRTPacket._get_exact(
                RT6DBodyPosition, data, component_position
            )
            component_position, matrix = QRTPacket._get_tuple(
                RT6DBodyRotation, data, component_position
            )
            append_components((position, matrix))
        return components