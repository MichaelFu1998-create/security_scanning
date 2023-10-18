def parsemail(raw_message):
    """Parse message headers, then remove BCC header."""
    message = email.parser.Parser().parsestr(raw_message)

    # Detect encoding
    detected = chardet.detect(bytearray(raw_message, "utf-8"))
    encoding = detected["encoding"]
    print(">>> encoding {}".format(encoding))
    for part in message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        part.set_charset(encoding)

    # Extract recipients
    addrs = email.utils.getaddresses(message.get_all("TO", [])) + \
        email.utils.getaddresses(message.get_all("CC", [])) + \
        email.utils.getaddresses(message.get_all("BCC", []))
    recipients = [x[1] for x in addrs]
    message.__delitem__("bcc")
    message.__setitem__('Date', email.utils.formatdate())
    sender = message["from"]

    return (message, sender, recipients)