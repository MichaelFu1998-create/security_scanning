def consume_message(
        method):
    """
    Decorator for methods handling requests from RabbitMQ

    The goal of this decorator is to perform the tasks common to all
    methods handling requests:

    - Log the raw message to *stdout*
    - Decode the message into a Python dictionary
    - Log errors to *stderr*
    - Signal the broker that we're done handling the request

    The method passed in will be called with the message body as a
    dictionary. It is assumed here that the message body is a JSON string
    encoded in UTF8.
    """

    def wrapper(
            self,
            channel,
            method_frame,
            header_frame,
            body):

        # Log the message
        sys.stdout.write("received message: {}\n".format(body))
        sys.stdout.flush()

        try:

            # Grab the data and call the method
            body = body.decode("utf-8")
            data = json.loads(body)
            method(self, data)

        except Exception as exception:

            # Log the error message
            sys.stderr.write("{}\n".format(traceback.format_exc()))
            sys.stderr.flush()


        # Signal the broker we are done
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    return wrapper