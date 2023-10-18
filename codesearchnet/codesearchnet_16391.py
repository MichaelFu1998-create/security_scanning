def get_force(self, component_info=None, data=None, component_position=None):
        """Get force data."""
        components = []
        append_components = components.append
        for _ in range(component_info.plate_count):
            component_position, plate = QRTPacket._get_exact(
                RTForcePlate, data, component_position
            )
            force_list = []
            for _ in range(plate.force_count):
                component_position, force = QRTPacket._get_exact(
                    RTForce, data, component_position
                )
                force_list.append(force)
            append_components((plate, force_list))
        return components