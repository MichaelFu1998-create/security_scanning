def get_analog_single(
        self, component_info=None, data=None, component_position=None
    ):
        """Get a single analog data channel."""
        components = []
        append_components = components.append
        for _ in range(component_info.device_count):
            component_position, device = QRTPacket._get_exact(
                RTAnalogDeviceSingle, data, component_position
            )

            RTAnalogDeviceSamples.format = struct.Struct(
                RTAnalogDeviceSamples.format_str % device.channel_count
            )
            component_position, sample = QRTPacket._get_tuple(
                RTAnalogDeviceSamples, data, component_position
            )
            append_components((device, sample))
        return components