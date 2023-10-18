def _create_transmissions(self, content_metadata_item_map):
        """
        Create ContentMetadataItemTransmision models for the given content metadata items.
        """
        # pylint: disable=invalid-name
        ContentMetadataItemTransmission = apps.get_model(
            'integrated_channel',
            'ContentMetadataItemTransmission'
        )
        transmissions = []
        for content_id, channel_metadata in content_metadata_item_map.items():
            transmissions.append(
                ContentMetadataItemTransmission(
                    enterprise_customer=self.enterprise_configuration.enterprise_customer,
                    integrated_channel_code=self.enterprise_configuration.channel_code(),
                    content_id=content_id,
                    channel_metadata=channel_metadata
                )
            )
        ContentMetadataItemTransmission.objects.bulk_create(transmissions)