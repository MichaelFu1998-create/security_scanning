def listen(self, reactor, endpoint_description):
        """
        Run the server, i.e. start listening for requests on the given host and
        port.

        :param reactor: The ``IReactorTCP`` to use.
        :param endpoint_description:
            The Twisted description for the endpoint to listen on.
        :return:
            A deferred that returns an object that provides ``IListeningPort``.
        """
        endpoint = serverFromString(reactor, endpoint_description)
        return endpoint.listen(Site(self.app.resource()))