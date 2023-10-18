def _transmit_update(self, channel_metadata_item_map, transmission_map):
        """
        Transmit content metadata update to integrated channel.
        """
        for chunk in chunks(channel_metadata_item_map, self.enterprise_configuration.transmission_chunk_size):
            serialized_chunk = self._serialize_items(list(chunk.values()))
            try:
                self.client.update_content_metadata(serialized_chunk)
            except ClientError as exc:
                LOGGER.error(
                    'Failed to update [%s] content metadata items for integrated channel [%s] [%s]',
                    len(chunk),
                    self.enterprise_configuration.enterprise_customer.name,
                    self.enterprise_configuration.channel_code,
                )
                LOGGER.error(exc)
            else:
                self._update_transmissions(chunk, transmission_map)