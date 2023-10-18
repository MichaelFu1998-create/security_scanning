def _delete_transmissions(self, content_metadata_item_ids):
        """
        Delete ContentMetadataItemTransmision models associated with the given content metadata items.
        """
        # pylint: disable=invalid-name
        ContentMetadataItemTransmission = apps.get_model(
            'integrated_channel',
            'ContentMetadataItemTransmission'
        )
        ContentMetadataItemTransmission.objects.filter(
            enterprise_customer=self.enterprise_configuration.enterprise_customer,
            integrated_channel_code=self.enterprise_configuration.channel_code(),
            content_id__in=content_metadata_item_ids
        ).delete()