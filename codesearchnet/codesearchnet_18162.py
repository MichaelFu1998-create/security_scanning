def get_response_data(self, response, parse_json=True):
        """
        Get response data or throw an appropiate exception
        :param response: requests response object
        :param parse_json: if True, response will be parsed as JSON
        :return: response data, either as json or as a regular response.content object
        """
        if response.status_code in (requests.codes.ok, requests.codes.created):
            if parse_json:
                return response.json()
            return response.content
        elif response.status_code == requests.codes.bad_request:
            response_json = response.json()
            raise BadRequestException(response_json.get("error", False) or response_json.get("errors",
                                                                                             _("Bad Request: {text}").format(text=response.text)))
        elif response.status_code == requests.codes.not_found:
            raise NotFoundException(_("Resource not found: {url}").format(url=response.url))
        elif response.status_code == requests.codes.internal_server_error:
            raise ServerErrorException(_("Internal server error"))
        elif response.status_code in (requests.codes.unauthorized, requests.codes.forbidden):
            raise AuthErrorException(_("Access denied"))
        elif response.status_code == requests.codes.too_many_requests:
            raise RateLimitException(_(response.text))
        else:
            raise ServerErrorException(_("Unknown error occurred"))