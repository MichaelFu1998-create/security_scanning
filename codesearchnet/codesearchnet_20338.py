def format_request_url(self, resource, *args):
        """create request url for resource"""
        return '/'.join((self.api_url, self.api_version, resource) +
                        tuple(str(x) for x in args))