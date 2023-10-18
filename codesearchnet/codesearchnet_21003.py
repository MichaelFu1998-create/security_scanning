def merge_text(events):
    """merges each run of successive text events into one text event"""
    text = []
    for obj in events:
        if obj['type'] == TEXT:
            text.append(obj['text'])
        else:
            if text:
                yield {'type': TEXT, 'text': ''.join(text)}
                text.clear()
            yield obj
    if text:
        yield {'type': TEXT, 'text': ''.join(text)}