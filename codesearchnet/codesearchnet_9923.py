def aggregate_history(self, ip, days_limit=None):
        """
            Get the full history of an IP, aggregate the result instead of
            returning one line per day.

            :param ip: IP address to search for
            :param days_limit: Max amount of days to query. (None means no limit)

            :rtype: list. For each change: FirstDay, LastDay, ASN, Block
        """
        first_date = None
        last_date = None
        prec_asn = None
        prec_block = None
        for entry in self.history(ip, days_limit):
            if entry is None:
                continue
            date, asn, block = entry
            if first_date is None:
                last_date = date
                first_date = date
                prec_asn = asn
                prec_block = block
            elif prec_asn == asn and prec_block == block:
                first_date = date
            else:
                yield first_date, last_date, prec_asn, prec_block
                last_date = date
                first_date = date
                prec_asn = asn
                prec_block = block
        if first_date is not None:
            yield first_date, last_date, prec_asn, prec_block