async def send_xml(self, xml):
        """Used to update QTM settings, see QTM RT protocol for more information.

        :param xml: XML document as a str. See QTM RT Documentation for details.
        """
        return await asyncio.wait_for(
            self._protocol.send_command(xml, command_type=QRTPacketType.PacketXML),
            timeout=self._timeout,
        )