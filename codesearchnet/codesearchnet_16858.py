def _parse_response(self, response):
        """Parses the API response and raises appropriate errors if
        raise_errors was set to True
        """
        if not self._raise_errors:
            return response

        is_4xx_error = str(response.status_code)[0] == '4'
        is_5xx_error = str(response.status_code)[0] == '5'
        content = response.content

        if response.status_code == 403:
            raise AuthenticationError(content)
        elif is_4xx_error:
            raise APIError(content)
        elif is_5xx_error:
            raise ServerError(content)

        return response