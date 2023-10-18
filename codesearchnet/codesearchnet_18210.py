def health(self, request):
        """ Listens to incoming health checks from Marathon on ``/health``. """
        if self.health_handler is None:
            return self._no_health_handler(request)

        health = self.health_handler()
        response_code = OK if health.healthy else SERVICE_UNAVAILABLE
        request.setResponseCode(response_code)
        write_request_json(request, health.json_message)