def add_arguments(self, parser):
        """
        Adds the optional arguments: ``--enterprise_customer``, ``--channel``
        """
        parser.add_argument(
            '--enterprise_customer',
            dest='enterprise_customer',
            default=None,
            metavar='ENTERPRISE_CUSTOMER_UUID',
            help=_('Transmit data for only this EnterpriseCustomer. '
                   'Omit this option to transmit to all EnterpriseCustomers with active integrated channels.'),
        )
        parser.add_argument(
            '--channel',
            dest='channel',
            default='',
            metavar='INTEGRATED_CHANNEL',
            help=_('Transmit data to this IntegrateChannel. '
                   'Omit this option to transmit to all configured, active integrated channels.'),
            choices=INTEGRATED_CHANNEL_CHOICES.keys(),
        )