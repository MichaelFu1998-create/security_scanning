def unscan(events, nsmap=None):
    """Converts events stream into lXML tree"""

    root = None
    last_closed_elt = None
    stack = []
    for obj in events:

        if obj['type'] == ENTER:
            elt = _obj2elt(obj, nsmap=nsmap)
            if stack:
                stack[-1].append(elt)
            elif root is not None:
                raise RuntimeError('Event stream tried to create second XML tree')
            else:
                root = elt
            stack.append(elt)
            last_closed_elt = None

        elif obj['type'] == EXIT:
            last_closed_elt = stack.pop()

        elif obj['type'] == COMMENT:
            elt = et.Comment(obj['text'])
            stack[-1].append(elt)

        elif obj['type'] == PI:
            elt = et.PI(obj['target'])
            if obj.get('text'):
                elt.text = obj['text']
            stack[-1].append(elt)

        elif obj['type'] == TEXT:
            text = obj['text']
            if text:
                if last_closed_elt is None:
                    stack[-1].text = (stack[-1].text or '') + text
                else:
                    last_closed_elt.tail = (last_closed_elt.tail or '') + text
        else:
            assert False, obj

    if root is None:
        raise RuntimeError('Empty XML event stream')

    return root