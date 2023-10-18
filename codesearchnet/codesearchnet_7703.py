def get_traffic_meter(self):
        """
        Return dict of traffic meter stats.

        Returns None if error occurred.
        """
        _LOGGER.info("Get traffic meter")

        def parse_text(text):
            """
                there are three kinds of values in the returned data
                This function parses the different values and returns
                (total, avg), timedelta or a plain float
            """
            def tofloats(lst): return (float(t) for t in lst)
            try:
                if "/" in text:  # "6.19/0.88" total/avg
                    return tuple(tofloats(text.split('/')))
                elif ":" in text:  # 11:14 hr:mn
                    hour, mins = tofloats(text.split(':'))
                    return timedelta(hours=hour, minutes=mins)
                else:
                    return float(text)
            except ValueError:
                return None

        success, response = self._make_request(SERVICE_DEVICE_CONFIG,
                                               "GetTrafficMeterStatistics")
        if not success:
            return None

        success, node = _find_node(
            response.text,
            ".//GetTrafficMeterStatisticsResponse")
        if not success:
            return None

        return {t.tag: parse_text(t.text) for t in node}