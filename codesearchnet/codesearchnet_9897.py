def _get_notify_msg_and_payload(result, stream):
    """Get notify message and payload dict"""
    token = stream.advance_past_chars(["=", "*"])
    token = int(token) if token != "" else None
    logger.debug("%s", fmt_green("parsing message"))
    message = stream.advance_past_chars([","])

    logger.debug("parsed message")
    logger.debug("%s", fmt_green(message))

    payload = _parse_dict(stream)
    return token, message.strip(), payload