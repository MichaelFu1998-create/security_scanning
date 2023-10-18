def get_skeletons(self, component_info=None, data=None, component_position=None):
        """Get skeletons
        """

        components = []
        append_components = components.append
        for _ in range(component_info.skeleton_count):
            component_position, info = QRTPacket._get_exact(
                RTSegmentCount, data, component_position
            )

            segments = []
            for __ in range(info.segment_count):
                component_position, segment = QRTPacket._get_exact(
                    RTSegmentId, data, component_position
                )
                component_position, position = QRTPacket._get_exact(
                    RTSegmentPosition, data, component_position
                )
                component_position, rotation = QRTPacket._get_exact(
                    RTSegmentRotation, data, component_position
                )

                segments.append((segment.id, position, rotation))
            append_components(segments)
        return components