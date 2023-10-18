def _before(self):
        """Records the starting time of this reqeust.
        """
        # Don't trace excluded routes.
        if request.path in self.excluded_routes:
            request._tracy_exclude = True
            return

        request._tracy_start_time = monotonic()
        client = request.headers.get(trace_header_client, None)
        require_client = current_app.config.get("TRACY_REQUIRE_CLIENT", False)
        if client is None and require_client:
            abort(400, "Missing %s header" % trace_header_client)

        request._tracy_client = client
        request._tracy_id = request.headers.get(trace_header_id, new_id())