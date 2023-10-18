def history(self, ip, days_limit=None):
        """
            Get the full history of an IP. It takes time.

            :param ip: IP address to search for
            :param days_limit: Max amount of days to query. (None means no limit)

            :rtype: list. For each day in the database: day, asn, block
        """
        all_dates = sorted(self.routing_db.smembers('imported_dates'), reverse=True)
        if days_limit is not None:
            all_dates = all_dates[:days_limit]
        return [self.date_asn_block(ip, date) for date in all_dates]