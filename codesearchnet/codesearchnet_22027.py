def to_delimited(header: Header, payload: Payload, side: CommSide) -> DelimitedMsg:
    """\
    Returns a message consisting of header frames, delimiter frame, and payload frames.
    The payload frames may be given as sequences of bytes (raw) or as `Message`s.
    """
    return raw_to_delimited(header, [side.serialize(msg) for msg in payload])