def _get_service(self):
        """Check mandatory service name parameter in POST request."""
        if "service" in self.document.attrib:
            value = self.document.attrib["service"].lower()
            if value in allowed_service_types:
                self.params["service"] = value
            else:
                raise OWSInvalidParameterValue("Service %s is not supported" % value, value="service")
        else:
            raise OWSMissingParameterValue('Parameter "service" is missing', value="service")
        return self.params["service"]