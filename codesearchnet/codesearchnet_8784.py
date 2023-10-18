def get_integrated_channels(self, options):
        """
        Generates a list of active integrated channels for active customers, filtered from the given options.

        Raises errors when invalid options are encountered.

        See ``add_arguments`` for the accepted options.
        """
        channel_classes = self.get_channel_classes(options.get('channel'))
        filter_kwargs = {
            'active': True,
            'enterprise_customer__active': True,
        }
        enterprise_customer = self.get_enterprise_customer(options.get('enterprise_customer'))
        if enterprise_customer:
            filter_kwargs['enterprise_customer'] = enterprise_customer

        for channel_class in channel_classes:
            for integrated_channel in channel_class.objects.filter(**filter_kwargs):
                yield integrated_channel