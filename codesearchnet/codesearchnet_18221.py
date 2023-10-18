def listen_events(self, reconnects=0):
        """
        Start listening for events from Marathon, running a sync when we first
        successfully subscribe and triggering a sync on API request events.
        """
        self.log.info('Listening for events from Marathon...')
        self._attached = False

        def on_finished(result, reconnects):
            # If the callback fires then the HTTP request to the event stream
            # went fine, but the persistent connection for the SSE stream was
            # dropped. Just reconnect for now- if we can't actually connect
            # then the errback will fire rather.
            self.log.warn('Connection lost listening for events, '
                          'reconnecting... ({reconnects} so far)',
                          reconnects=reconnects)
            reconnects += 1
            return self.listen_events(reconnects)

        def log_failure(failure):
            self.log.failure('Failed to listen for events', failure)
            return failure

        return self.marathon_client.get_events({
            'event_stream_attached': self._sync_on_event_stream_attached,
            'api_post_event': self._sync_on_api_post_event
        }).addCallbacks(on_finished, log_failure, callbackArgs=[reconnects])