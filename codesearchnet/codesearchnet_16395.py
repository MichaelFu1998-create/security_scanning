def get_image(self, component_info=None, data=None, component_position=None):
        """Get image."""
        components = []
        append_components = components.append
        for _ in range(component_info.image_count):
            component_position, image_info = QRTPacket._get_exact(
                RTImage, data, component_position
            )
            append_components((image_info, data[component_position:-1]))
        return components