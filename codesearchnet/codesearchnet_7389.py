def add_parameters(self, **params):
        """
        Add URL parameters
        Also ensure that only valid format/content combinations are requested
        """
        self.url_params = None
        # we want JSON by default
        if not params.get("format"):
            params["format"] = "json"
        # non-standard content must be retrieved as Atom
        if params.get("content"):
            params["format"] = "atom"
        # TODO: rewrite format=atom, content=json request
        if "limit" not in params or params.get("limit") == 0:
            params["limit"] = 100
        # Need ability to request arbitrary number of results for version
        # response
        # -1 value is hack that works with current version
        elif params["limit"] == -1 or params["limit"] is None:
            del params["limit"]
        # bib format can't have a limit
        if params.get("format") == "bib":
            del params["limit"]
        self.url_params = urlencode(params, doseq=True)