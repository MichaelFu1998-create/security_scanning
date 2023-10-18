def from_delimited(msgs: DelimitedMsg, side: CommSide) -> Msgs:
    """\
    From a message consisting of header frames, delimiter frame, and payload frames, return a tuple `(header, payload)`.
    The payload frames may be returned as sequences of bytes (raw) or as `Message`s.
    """
    header, raw_payload = raw_from_delimited(msgs)
    return header, tuple(side.parse(msg_raw) for msg_raw in raw_payload)