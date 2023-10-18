async def get_current_frame(self, components=None) -> QRTPacket:
        """Get measured values from QTM for a single frame.

        :param components: A list of components to receive, could be 'all' or any combination of
                '2d', '2dlin', '3d', '3dres', '3dnolabels',
                '3dnolabelsres', 'force', 'forcesingle', '6d', '6dres',
                '6deuler', '6deulerres', 'gazevector', 'image', 'timecode',
                'skeleton', 'skeleton:global'

        :rtype: A :class:`qtm.QRTPacket` containing requested components
        """

        if components is None:
            components = ["all"]
        else:
            _validate_components(components)

        cmd = "getcurrentframe %s" % " ".join(components)
        return await asyncio.wait_for(
            self._protocol.send_command(cmd), timeout=self._timeout
        )