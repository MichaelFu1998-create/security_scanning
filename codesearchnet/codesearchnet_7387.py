def _extract_links(self):
        """
        Extract self, first, next, last links from a request response
        """
        extracted = dict()
        try:
            for key, value in self.request.links.items():
                parsed = urlparse(value["url"])
                fragment = "{path}?{query}".format(path=parsed[2], query=parsed[4])
                extracted[key] = fragment
            # add a 'self' link
            parsed = list(urlparse(self.self_link))
            # strip 'format' query parameter
            stripped = "&".join(
                [
                    "%s=%s" % (p[0], p[1])
                    for p in parse_qsl(parsed[4])
                    if p[0] != "format"
                ]
            )
            # rebuild url fragment
            # this is a death march
            extracted["self"] = urlunparse(
                [parsed[0], parsed[1], parsed[2], parsed[3], stripped, parsed[5]]
            )
            return extracted
        except KeyError:
            # No links present, because it's a single item
            return None