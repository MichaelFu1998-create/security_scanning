def send_messages(cls, http_request, message_requests):
        """
        Deduplicate any outgoing message requests, and send the remainder.

        Args:
            http_request: The HTTP request in whose response we want to embed the messages
            message_requests: A list of undeduplicated messages in the form of tuples of message type
                and text- for example, ('error', 'Something went wrong')
        """
        deduplicated_messages = set(message_requests)
        for msg_type, text in deduplicated_messages:
            message_function = getattr(messages, msg_type)
            message_function(http_request, text)