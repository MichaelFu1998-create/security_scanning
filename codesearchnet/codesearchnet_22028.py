def raw_from_delimited(msgs: DelimitedMsg) -> RawMsgs:
    """\
    From a message consisting of header frames, delimiter frame, and payload frames, return a tuple `(header, payload)`.
    The payload frames may be returned as sequences of bytes (raw) or as `Message`s.
    """
    delim = _rindex(msgs, b'')
    return tuple(msgs[:delim]), tuple(msgs[delim + 1:])