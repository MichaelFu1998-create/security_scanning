def _get_param(self, param, allowed_values=None, optional=False):
        """Get parameter in GET request."""
        request_params = self._request_params()
        if param in request_params:
            value = request_params[param].lower()
            if allowed_values is not None:
                if value in allowed_values:
                    self.params[param] = value
                else:
                    raise OWSInvalidParameterValue("%s %s is not supported" % (param, value), value=param)
        elif optional:
            self.params[param] = None
        else:
            raise OWSMissingParameterValue('Parameter "%s" is missing' % param, value=param)
        return self.params[param]