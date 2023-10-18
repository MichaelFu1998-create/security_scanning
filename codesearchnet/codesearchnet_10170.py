def _get(self, route, headers=None, failure_message=None):
        """
        Execute a post request and return the result
        :param headers:
        :return:
        """
        headers = self._get_headers(headers)
        response_lambda = (
            lambda: requests.get(self._get_qualified_route(route), headers=headers, verify=False, proxies=self.proxies)
        )
        response = check_for_rate_limiting(response_lambda(), response_lambda)
        return self._handle_response(response, failure_message)