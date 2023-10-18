def transmit(self, payload, **kwargs):
        """
        Transmit content metadata items to the integrated channel.
        """
        items_to_create, items_to_update, items_to_delete, transmission_map = self._partition_items(payload)
        self._prepare_items_for_delete(items_to_delete)
        prepared_items = {}
        prepared_items.update(items_to_create)
        prepared_items.update(items_to_update)
        prepared_items.update(items_to_delete)

        skip_metadata_transmission = False

        for chunk in chunks(prepared_items, self.enterprise_configuration.transmission_chunk_size):
            chunked_items = list(chunk.values())
            if skip_metadata_transmission:
                # Remove the failed items from the create/update/delete dictionaries,
                # so ContentMetadataItemTransmission objects are not synchronized for
                # these items below.
                self._remove_failed_items(chunked_items, items_to_create, items_to_update, items_to_delete)
            else:
                try:
                    self.client.update_content_metadata(self._serialize_items(chunked_items))
                except ClientError as exc:
                    LOGGER.error(
                        'Failed to update [%s] content metadata items for integrated channel [%s] [%s]',
                        len(chunked_items),
                        self.enterprise_configuration.enterprise_customer.name,
                        self.enterprise_configuration.channel_code,
                    )
                    LOGGER.error(exc)

                    # Remove the failed items from the create/update/delete dictionaries,
                    # so ContentMetadataItemTransmission objects are not synchronized for
                    # these items below.
                    self._remove_failed_items(chunked_items, items_to_create, items_to_update, items_to_delete)

                    # SAP servers throttle incoming traffic, If a request fails than the subsequent would fail too,
                    # So, no need to keep trying and failing. We should stop here and retry later.
                    skip_metadata_transmission = True

        self._create_transmissions(items_to_create)
        self._update_transmissions(items_to_update, transmission_map)
        self._delete_transmissions(items_to_delete.keys())