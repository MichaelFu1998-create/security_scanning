def get_data(self, url, type=GET, params=None):
        """
            This method is a basic implementation of __call_api that checks
            errors too. In case of success the method will return True or the
            content of the response to the request.

            Pagination is automatically detected and handled accordingly
        """
        if params is None:
            params = dict()

        # If per_page is not set, make sure it has a sane default
        if type is GET:
            params.setdefault("per_page", 200)

        req = self.__perform_request(url, type, params)
        if req.status_code == 204:
            return True

        if req.status_code == 404:
            raise NotFoundError()

        try:
            data = req.json()
        except ValueError as e:
            raise JSONReadError(
                'Read failed from DigitalOcean: %s' % str(e)
            )

        if not req.ok:
            msg = [data[m] for m in ("id", "message") if m in data][1]
            raise DataReadError(msg)

        # init request limits
        self.__init_ratelimit(req.headers)

        # If there are more elements available (total) than the elements per
        # page, try to deal with pagination. Note: Breaking the logic on
        # multiple pages,
        pages = data.get("links", {}).get("pages", {})
        if pages.get("next") and "page" not in params:
            return self.__deal_with_pagination(url, type, params, data)
        else:
            return data