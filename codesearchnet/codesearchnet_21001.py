def parse(filename):
    """Parses file content into events stream"""
    for event, elt in et.iterparse(filename, events= ('start', 'end', 'comment', 'pi'), huge_tree=True):
        if event == 'start':
            obj = _elt2obj(elt)
            obj['type'] = ENTER
            yield obj
            if elt.text:
                yield {'type': TEXT, 'text': elt.text}
        elif event == 'end':
            yield {'type': EXIT}
            if elt.tail:
                yield {'type': TEXT, 'text': elt.tail}
            elt.clear()
        elif event == 'comment':
            yield {'type': COMMENT, 'text': elt.text}
        elif event == 'pi':
            yield {'type': PI, 'text': elt.text}
        else:
            assert False, (event, elt)