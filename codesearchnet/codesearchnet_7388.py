def _updated(self, url, payload, template=None):
        """
        Generic call to see if a template request returns 304
        accepts:
        - a string to combine with the API endpoint
        - a dict of format values, in case they're required by 'url'
        - a template name to check for
        As per the API docs, a template less than 1 hour old is
        assumed to be fresh, and will immediately return False if found
        """
        # If the template is more than an hour old, try a 304
        if (
            abs(
                datetime.datetime.utcnow().replace(tzinfo=pytz.timezone("GMT"))
                - self.templates[template]["updated"]
            ).seconds
            > 3600
        ):
            query = self.endpoint + url.format(
                u=self.library_id, t=self.library_type, **payload
            )
            headers = {
                "If-Modified-Since": payload["updated"].strftime(
                    "%a, %d %b %Y %H:%M:%S %Z"
                )
            }
            headers.update(self.default_headers())
            # perform the request, and check whether the response returns 304
            req = requests.get(query, headers=headers)
            try:
                req.raise_for_status()
            except requests.exceptions.HTTPError:
                error_handler(req)
            return req.status_code == 304
        # Still plenty of life left in't
        return False