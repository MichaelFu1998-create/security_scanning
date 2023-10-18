def notify_client(
        notifier_uri,
        client_id,
        status_code,
        message=None):
    """
    Notify the client of the result of handling a request

    The payload contains two elements:

    - client_id
    - result

    The *client_id* is the id of the client to notify. It is assumed
    that the notifier service is able to identify the client by this id
    and that it can pass the *result* to it.

    The *result* always contains a *status_code* element. In case the
    message passed in is not None, it will also contain a *message*
    element.

    In case the notifier service does not exist or returns an error,
    an error message will be logged to *stderr*.
    """
    payload = {
        "client_id": client_id,
        "result": {
            "response": {
                "status_code": status_code
            }
        }
    }

    if message is not None:
        payload["result"]["response"]["message"] = message

    response = requests.post(notifier_uri, json=payload)

    if response.status_code != 201:
        sys.stderr.write("failed to notify client: {}\n".format(payload))
        sys.stderr.flush()