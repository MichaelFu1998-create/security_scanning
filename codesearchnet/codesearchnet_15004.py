def _get_request_type(self):
        """Find requested request type in POST request."""
        value = self.document.tag.lower()
        if value in allowed_request_types[self.params['service']]:
            self.params["request"] = value
        else:
            raise OWSInvalidParameterValue("Request type %s is not supported" % value, value="request")
        return self.params["request"]