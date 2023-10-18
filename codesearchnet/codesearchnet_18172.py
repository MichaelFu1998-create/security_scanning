def show_response_messages(response_json):
    """
    Show all messages in the `messages` key of the given dict.
    """
    message_type_kwargs = {
        'warning': {'fg': 'yellow'},
        'error': {'fg': 'red'},
    }
    for message in response_json.get('messages', []):
        click.secho(message['text'], **message_type_kwargs.get(message['type'], {}))