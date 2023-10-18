def get_events(self, callbacks):
        """
        Attach to Marathon's event stream using Server-Sent Events (SSE).

        :param callbacks:
            A dict mapping event types to functions that handle the event data
        """
        d = self.request(
            'GET', path='/v2/events', unbuffered=True,
            # The event_type parameter was added in Marathon 1.3.7. It can be
            # used to specify which event types we are interested in. On older
            # versions of Marathon it is ignored, and we ignore events we're
            # not interested in anyway.
            params={'event_type': sorted(callbacks.keys())},
            headers={
                'Accept': 'text/event-stream',
                'Cache-Control': 'no-store'
            })

        def handler(event, data):
            callback = callbacks.get(event)
            # Deserialize JSON if a callback is present
            if callback is not None:
                callback(json.loads(data))

        return d.addCallback(
            sse_content, handler, reactor=self._reactor, **self._sse_kwargs)