def _delete(self, route, headers=None, failure_message=None):
        """
        Execute a delete request and return the result
        :param headers:
        :return:
        """
        headers = self._get_headers(headers)
        response_lambda = (lambda: requests.delete(
            self._get_qualified_route(route), headers=headers, verify=False, proxies=self.proxies)
                           )
        response = check_for_rate_limiting(response_lambda(), response_lambda)
        return self._handle_response(response, failure_message)