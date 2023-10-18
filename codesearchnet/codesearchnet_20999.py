def scan(xml):
    """Converts XML tree to event generator"""

    if xml.tag is et.Comment:
        yield {'type': COMMENT, 'text': xml.text}
        return

    if xml.tag is et.PI:
        if xml.text:
            yield {'type': PI, 'target': xml.target, 'text': xml.text}
        else:
            yield {'type': PI, 'target': xml.target}
        return

    obj = _elt2obj(xml)
    obj['type'] = ENTER
    yield obj

    assert type(xml.tag) is str, xml
    if xml.text:
        yield {'type': TEXT, 'text': xml.text}

    for c in xml:
        for x in scan(c): yield x
        if c.tail:
            yield {'type': TEXT, 'text': c.tail}

    yield {'type': EXIT}