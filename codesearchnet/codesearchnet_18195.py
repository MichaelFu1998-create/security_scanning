def _check_request_results(self, results):
        """
        Check the result of each request that we made. If a failure occurred,
        but some requests succeeded, log and count the failures. If all
        requests failed, raise an error.

        :return:
            The list of responses, with a None value for any requests that
            failed.
        """
        responses = []
        failed_endpoints = []
        for index, result_tuple in enumerate(results):
            success, result = result_tuple
            if success:
                responses.append(result)
            else:
                endpoint = self.endpoints[index]
                self.log.failure(
                    'Failed to make a request to a marathon-lb instance: '
                    '{endpoint}', result, LogLevel.error, endpoint=endpoint)
                responses.append(None)
                failed_endpoints.append(endpoint)

        if len(failed_endpoints) == len(self.endpoints):
            raise RuntimeError(
                'Failed to make a request to all marathon-lb instances')

        if failed_endpoints:
            self.log.error(
                'Failed to make a request to {x}/{y} marathon-lb instances: '
                '{endpoints}', x=len(failed_endpoints), y=len(self.endpoints),
                endpoints=failed_endpoints)

        return responses