def asn(self, ip, announce_date=None):
        """
            Give an IP, maybe a date, get the ASN.
            This is the fastest command.

            :param ip: IP address to search for
            :param announce_date: Date of the announcement

            :rtype: String, ASN.

        """
        assignations, announce_date, _ = self.run(ip, announce_date)
        return next((assign for assign in assignations if assign is not None), None), announce_date