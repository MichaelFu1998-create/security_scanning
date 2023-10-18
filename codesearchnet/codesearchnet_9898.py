def _get_result_msg_and_payload(result, stream):
    """Get result message and payload dict"""

    groups = _GDB_MI_RESULT_RE.match(result).groups()
    token = int(groups[0]) if groups[0] != "" else None
    message = groups[1]

    if groups[2] is None:
        payload = None
    else:
        stream.advance_past_chars([","])
        payload = _parse_dict(stream)

    return token, message, payload