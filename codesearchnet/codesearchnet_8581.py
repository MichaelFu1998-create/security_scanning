def _get_transmissions(self):
        """
        Return the ContentMetadataItemTransmision models for previously
        transmitted content metadata items.
        """
        # pylint: disable=invalid-name
        ContentMetadataItemTransmission = apps.get_model(
            'integrated_channel',
            'ContentMetadataItemTransmission'
        )
        return ContentMetadataItemTransmission.objects.filter(
            enterprise_customer=self.enterprise_configuration.enterprise_customer,
            integrated_channel_code=self.enterprise_configuration.channel_code()
        )