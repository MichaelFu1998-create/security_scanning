def upstream_url(self, uri):
        "Returns the URL to the upstream data source for the given URI based on configuration"
        return self.application.options.upstream + self.request.uri