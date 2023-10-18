def _parse_datapoints(self, parsed_duration, parsed_resolution, limit):
        """
        Parse the number of datapoints of a query.
        This can be calculated from the given duration and resolution of the query.
        E.g. if the query has a duation of 2*60*60 = 7200 seconds and a resolution of 10 seconds
        then the number of datapoints would be 7200/10 => 7200 datapoints.

        :param parsed_duration:
        :param parsed_resolution:
        :param limit:
        :return:
        """
        return self.datapoints_parser.parse(parsed_duration, parsed_resolution, limit)