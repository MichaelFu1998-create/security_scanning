def _partition_items(self, channel_metadata_item_map):
        """
        Return items that need to be created, updated, and deleted along with the
        current ContentMetadataItemTransmissions.
        """
        items_to_create = {}
        items_to_update = {}
        items_to_delete = {}
        transmission_map = {}
        export_content_ids = channel_metadata_item_map.keys()

        # Get the items that were previously transmitted to the integrated channel.
        # If we are not transmitting something that was previously transmitted,
        # we need to delete it from the integrated channel.
        for transmission in self._get_transmissions():
            transmission_map[transmission.content_id] = transmission
            if transmission.content_id not in export_content_ids:
                items_to_delete[transmission.content_id] = transmission.channel_metadata

        # Compare what is currently being transmitted to what was transmitted
        # previously, identifying items that need to be created or updated.
        for item in channel_metadata_item_map.values():
            content_id = item.content_id
            channel_metadata = item.channel_metadata
            transmitted_item = transmission_map.get(content_id, None)
            if transmitted_item is not None:
                if diff(channel_metadata, transmitted_item.channel_metadata):
                    items_to_update[content_id] = channel_metadata
            else:
                items_to_create[content_id] = channel_metadata

        LOGGER.info(
            'Preparing to transmit creation of [%s] content metadata items with plugin configuration [%s]: [%s]',
            len(items_to_create),
            self.enterprise_configuration,
            items_to_create.keys(),
        )
        LOGGER.info(
            'Preparing to transmit update of [%s] content metadata items with plugin configuration [%s]: [%s]',
            len(items_to_update),
            self.enterprise_configuration,
            items_to_update.keys(),
        )
        LOGGER.info(
            'Preparing to transmit deletion of [%s] content metadata items with plugin configuration [%s]: [%s]',
            len(items_to_delete),
            self.enterprise_configuration,
            items_to_delete.keys(),
        )

        return items_to_create, items_to_update, items_to_delete, transmission_map