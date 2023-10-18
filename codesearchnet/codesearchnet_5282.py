def _mpsse_sync(self, max_retries=10):
        """Synchronize buffers with MPSSE by sending bad opcode and reading expected
        error response.  Should be called once after enabling MPSSE."""
        # Send a bad/unknown command (0xAB), then read buffer until bad command
        # response is found.
        self._write('\xAB')
        # Keep reading until bad command response (0xFA 0xAB) is returned.
        # Fail if too many read attempts are made to prevent sticking in a loop.
        tries = 0
        sync = False
        while not sync:
            data = self._poll_read(2)
            if data == '\xFA\xAB':
                sync = True
            tries += 1
            if tries >= max_retries:
                raise RuntimeError('Could not synchronize with FT232H!')