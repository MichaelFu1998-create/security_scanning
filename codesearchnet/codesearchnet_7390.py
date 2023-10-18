def _build_query(self, query_string, no_params=False):
        """
        Set request parameters. Will always add the user ID if it hasn't
        been specifically set by an API method
        """
        try:
            query = quote(query_string.format(u=self.library_id, t=self.library_type))
        except KeyError as err:
            raise ze.ParamNotPassed("There's a request parameter missing: %s" % err)
        # Add the URL parameters and the user key, if necessary
        if no_params is False:
            if not self.url_params:
                self.add_parameters()
            query = "%s?%s" % (query, self.url_params)
        return query