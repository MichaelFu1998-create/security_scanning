async def stream_frames_stop(self):
        """Stop streaming frames."""

        self._protocol.set_on_packet(None)

        cmd = "streamframes stop"
        await self._protocol.send_command(cmd, callback=False)