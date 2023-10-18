def _update_transmissions(self, content_metadata_item_map, transmission_map):
        """
        Update ContentMetadataItemTransmision models for the given content metadata items.
        """
        for content_id, channel_metadata in content_metadata_item_map.items():
            transmission = transmission_map[content_id]
            transmission.channel_metadata = channel_metadata
            transmission.save()