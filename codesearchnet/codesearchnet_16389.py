def get_analog(self, component_info=None, data=None, component_position=None):
        """Get analog data."""
        components = []
        append_components = components.append
        for _ in range(component_info.device_count):
            component_position, device = QRTPacket._get_exact(
                RTAnalogDevice, data, component_position
            )
            if device.sample_count > 0:
                component_position, sample_number = QRTPacket._get_exact(
                    RTSampleNumber, data, component_position
                )

                RTAnalogChannel.format = struct.Struct(
                    RTAnalogChannel.format_str % device.sample_count
                )
                for _ in range(device.channel_count):
                    component_position, channel = QRTPacket._get_tuple(
                        RTAnalogChannel, data, component_position
                    )
                    append_components((device, sample_number, channel))

        return components