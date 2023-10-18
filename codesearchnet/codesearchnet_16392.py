def get_force_single(self, component_info=None, data=None, component_position=None):
        """Get a single force data channel."""
        components = []
        append_components = components.append
        for _ in range(component_info.plate_count):
            component_position, plate = QRTPacket._get_exact(
                RTForcePlateSingle, data, component_position
            )
            component_position, force = QRTPacket._get_exact(
                RTForce, data, component_position
            )
            append_components((plate, force))
        return components