def parse(packet):
    """
    Parses an APRS packet and returns a dict with decoded data

    - All attributes are in metric units
    """

    if not isinstance(packet, string_type_parse):
        raise TypeError("Expected packet to be str/unicode/bytes, got %s", type(packet))

    if len(packet) == 0:
        raise ParseError("packet is empty", packet)

    # attempt to detect encoding
    if isinstance(packet, bytes):
        packet = _unicode_packet(packet)

    packet = packet.rstrip("\r\n")
    logger.debug("Parsing: %s", packet)

    # split into head and body
    try:
        (head, body) = packet.split(':', 1)
    except:
        raise ParseError("packet has no body", packet)

    if len(body) == 0:
        raise ParseError("packet body is empty", packet)

    parsed = {
        'raw': packet,
        }

    # parse head
    try:
        parsed.update(parse_header(head))
    except ParseError as msg:
        raise ParseError(str(msg), packet)

    # parse body
    packet_type = body[0]
    body = body[1:]

    if len(body) == 0 and packet_type != '>':
        raise ParseError("packet body is empty after packet type character", packet)

    # attempt to parse the body
    try:
        _try_toparse_body(packet_type, body, parsed)

    # capture ParseErrors and attach the packet
    except (UnknownFormat, ParseError) as exp:
        exp.packet = packet
        raise

    # if we fail all attempts to parse, try beacon packet
    if 'format' not in parsed:
        if not re.match(r"^(AIR.*|ALL.*|AP.*|BEACON|CQ.*|GPS.*|DF.*|DGPS.*|"
                        "DRILL.*|DX.*|ID.*|JAVA.*|MAIL.*|MICE.*|QST.*|QTH.*|"
                        "RTCM.*|SKY.*|SPACE.*|SPC.*|SYM.*|TEL.*|TEST.*|TLM.*|"
                        "WX.*|ZIP.*|UIDIGI)$", parsed['to']):
            raise UnknownFormat("format is not supported", packet)

        parsed.update({
            'format': 'beacon',
            'text': packet_type + body,
            })

    logger.debug("Parsed ok.")
    return parsed