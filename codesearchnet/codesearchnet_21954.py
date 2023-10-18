def consume_message_with_notify(
        notifier_uri_getter):
    """
    Decorator for methods handling requests from RabbitMQ

    This decorator builds on the :py:func:`consume_message` decorator. It extents
    it by logic for notifying a client of the result of handling the
    request.

    The *notifier_uri_getter* argument must be a callable which accepts
    *self* and returns the uri of the notifier service.
    """

    def consume_message_with_notify_decorator(
            method):

        @consume_message
        def wrapper(
                self,
                data):

            notifier_uri = notifier_uri_getter(self)
            client_id = data["client_id"]

            # Forward the call to the method and notify the client of the
            # result
            try:
                method(self, data)
                notify_client(notifier_uri, client_id, 200)
            except Exception as exception:
                notify_client(notifier_uri, client_id, 400, str(exception))
                raise

        return wrapper

    return consume_message_with_notify_decorator