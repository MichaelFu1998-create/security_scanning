def run(self):
        """ Called by the process, it runs it.

        NEVER call this method directly. Instead call start() to start the separate process.
        If you don't want to use a second process, then call fetch() directly on this istance.

        To stop, call terminate()
        """

        producer_deferred = defer.Deferred()
        producer_deferred.addCallback(self._request_finished)
        producer_deferred.addErrback(self._request_error)

        receiver_deferred = defer.Deferred()
        receiver_deferred.addCallback(self._response_finished)
        receiver_deferred.addErrback(self._response_error)

        self._producer = producer.MultiPartProducer(
            self._files,
            self._data,
            callback = self._request_progress,
            deferred = producer_deferred
        )
        self._receiver = receiver.StringReceiver(receiver_deferred)

        headers = {
            'Content-Type': "multipart/form-data; boundary=%s" % self._producer.boundary
        }

        self._reactor, request = self._connection.build_twisted_request(
            "POST",
            "room/%s/uploads" % self._room.id,
            extra_headers = headers,
            body_producer = self._producer
        )

        request.addCallback(self._response)
        request.addErrback(self._shutdown)

        self._reactor.run()