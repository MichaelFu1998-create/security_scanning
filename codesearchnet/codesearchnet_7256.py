async def _on_push_data(self, data_bytes):
        """Parse push data and trigger events."""
        logger.debug('Received chunk:\n{}'.format(data_bytes))
        for chunk in self._chunk_parser.get_chunks(data_bytes):

            # Consider the channel connected once the first chunk is received.
            if not self._is_connected:
                if self._on_connect_called:
                    self._is_connected = True
                    await self.on_reconnect.fire()
                else:
                    self._on_connect_called = True
                    self._is_connected = True
                    await self.on_connect.fire()

            # chunk contains a container array
            container_array = json.loads(chunk)
            # container array is an array of inner arrays
            for inner_array in container_array:
                # inner_array always contains 2 elements, the array_id and the
                # data_array.
                array_id, data_array = inner_array
                logger.debug('Chunk contains data array with id %r:\n%r',
                             array_id, data_array)
                await self.on_receive_array.fire(data_array)