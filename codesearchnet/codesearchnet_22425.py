def _after(self, response):
        """Calculates the request duration, and adds a transaction
        ID to the header.
        """
        # Ignore excluded routes.
        if getattr(request, '_tracy_exclude', False):
            return response

        duration = None
        if getattr(request, '_tracy_start_time', None):
            duration = monotonic() - request._tracy_start_time

        # Add Trace_ID header.
        trace_id = None
        if getattr(request, '_tracy_id', None):
            trace_id = request._tracy_id
            response.headers[trace_header_id] = trace_id

        # Get the invoking client.
        trace_client = None
        if getattr(request, '_tracy_client', None):
            trace_client = request._tracy_client

        # Extra log kwargs.
        d = {'status_code': response.status_code,
             'url': request.base_url,
             'client_ip': request.remote_addr,
             'trace_name': trace_client,
             'trace_id': trace_id,
             'trace_duration': duration}
        logger.info(None, extra=d)
        return response