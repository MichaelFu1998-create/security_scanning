async def _on_receive_array(self, array):
        """Parse channel array and call the appropriate events."""
        if array[0] == 'noop':
            pass  # This is just a keep-alive, ignore it.
        else:
            wrapper = json.loads(array[0]['p'])
            # Wrapper appears to be a Protocol Buffer message, but encoded via
            # field numbers as dictionary keys. Since we don't have a parser
            # for that, parse it ad-hoc here.
            if '3' in wrapper:
                # This is a new client_id.
                self._client_id = wrapper['3']['2']
                logger.info('Received new client_id: %r', self._client_id)
                # Once client_id is received, the channel is ready to have
                # services added.
                await self._add_channel_services()
            if '2' in wrapper:
                pblite_message = json.loads(wrapper['2']['2'])
                if pblite_message[0] == 'cbu':
                    # This is a (Client)BatchUpdate containing StateUpdate
                    # messages.
                    batch_update = hangouts_pb2.BatchUpdate()
                    pblite.decode(batch_update, pblite_message,
                                  ignore_first_item=True)
                    for state_update in batch_update.state_update:
                        logger.debug('Received StateUpdate:\n%s', state_update)
                        header = state_update.state_update_header
                        self._active_client_state = header.active_client_state
                        await self.on_state_update.fire(state_update)
                else:
                    logger.info('Ignoring message: %r', pblite_message[0])