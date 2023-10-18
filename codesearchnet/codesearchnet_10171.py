def _post(self, route, data, headers=None, failure_message=None):
        """
        Execute a post request and return the result
        :param data:
        :param headers:
        :return:
        """
        headers = self._get_headers(headers)
        response_lambda = (
            lambda: requests.post(
                self._get_qualified_route(route), headers=headers, data=data, verify=False, proxies=self.proxies
            )
        )
        response = check_for_rate_limiting(response_lambda(), response_lambda)
        return self._handle_response(response, failure_message)