def date_asn_block(self, ip, announce_date=None):
        """
            Get the ASN and the IP Block announcing the IP at a specific date.

            :param ip: IP address to search for
            :param announce_date: Date of the announcement

            :rtype: tuple

                .. code-block:: python

                    (announce_date, asn, block)

            .. note::

                the returned announce_date might be different of the one
                given in parameter because some raw files are missing and we
                don't have the information. In this case, the nearest known
                date will be chosen,
        """
        assignations, announce_date, keys = self.run(ip, announce_date)
        pos = next((i for i, j in enumerate(assignations) if j is not None), None)
        if pos is not None:
            block = keys[pos]
            if block != '0.0.0.0/0':
                return announce_date, assignations[pos], block
        return None