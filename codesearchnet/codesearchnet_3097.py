def split_at_any(text,
                 lis,
                 translate=False,
                 not_before=[],
                 not_after=[],
                 validitate=None):
    """ doc """
    lis.sort(key=lambda x: len(x), reverse=True)
    last = 0
    n = 0
    text_len = len(text)
    while n < text_len:
        if any(text[:n].endswith(e)
               for e in not_before):  #Cant end with end before
            n += 1
            continue
        for e in lis:
            s = len(e)
            if s + n > text_len:
                continue
            if validitate and not validitate(e, text[:n], text[n + s:]):
                continue
            if any(text[n + s:].startswith(e)
                   for e in not_after):  #Cant end with end before
                n += 1
                break
            if e == text[n:n + s]:
                yield text[last:n] if not translate else translate(
                    text[last:n])
                yield e
                n += s
                last = n
                break
        else:
            n += 1
    yield text[last:n] if not translate else translate(text[last:n])