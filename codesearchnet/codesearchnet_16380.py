async def take_control(self, password):
        """Take control of QTM.

        :param password: Password as entered in QTM.
        """
        cmd = "takecontrol %s" % password
        return await asyncio.wait_for(
            self._protocol.send_command(cmd), timeout=self._timeout
        )