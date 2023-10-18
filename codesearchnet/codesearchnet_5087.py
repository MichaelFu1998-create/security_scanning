def cleanup_text (text):
    """
    It scrubs the garbled from its stream...
    Or it gets the debugger again.
    """
    x = " ".join(map(lambda s: s.strip(), text.split("\n"))).strip()

    x = x.replace('“', '"').replace('”', '"')
    x = x.replace("‘", "'").replace("’", "'").replace("`", "'")
    x = x.replace('…', '...').replace('–', '-')

    x = str(unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('ascii'))

    # some content returns text in bytes rather than as a str ?
    try:
        assert type(x).__name__ == 'str'
    except AssertionError:
        print("not a string?", type(line), line)

    return x