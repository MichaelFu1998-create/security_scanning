def make_message_multipart(message):
    """Convert a message into a multipart message."""
    if not message.is_multipart():
        multipart_message = email.mime.multipart.MIMEMultipart('alternative')
        for header_key in set(message.keys()):
            # Preserve duplicate headers
            values = message.get_all(header_key, failobj=[])
            for value in values:
                multipart_message[header_key] = value
        original_text = message.get_payload()
        multipart_message.attach(email.mime.text.MIMEText(original_text))
        message = multipart_message
    # HACK: For Python2 (see comments in `_create_boundary`)
    message = _create_boundary(message)
    return message