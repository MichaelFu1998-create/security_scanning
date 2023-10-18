def convert_markdown(message):
    """Convert markdown in message text to HTML."""
    assert message['Content-Type'].startswith("text/markdown")
    del message['Content-Type']
    # Convert the text from markdown and then make the message multipart
    message = make_message_multipart(message)
    for payload_item in set(message.get_payload()):
        # Assume the plaintext item is formatted with markdown.
        # Add corresponding HTML version of the item as the last part of
        # the multipart message (as per RFC 2046)
        if payload_item['Content-Type'].startswith('text/plain'):
            original_text = payload_item.get_payload()
            html_text = markdown.markdown(original_text)
            html_payload = future.backports.email.mime.text.MIMEText(
                "<html><body>{}</body></html>".format(html_text),
                "html",
            )
            message.attach(html_payload)
    return message