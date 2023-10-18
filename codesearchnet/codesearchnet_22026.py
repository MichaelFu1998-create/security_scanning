def raw_to_delimited(header: Header, raw_payload: RawPayload) -> DelimitedMsg:
    """\
    Returns a message consisting of header frames, delimiter frame, and payload frames.
    The payload frames may be given as sequences of bytes (raw) or as `Message`s.
    """
    return tuple(header) + (b'',) + tuple(raw_payload)