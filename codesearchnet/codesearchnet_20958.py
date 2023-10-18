def _filename(draw, result_type=None):
    """Generate a path value of type result_type.

    result_type can either be bytes or text_type

    """
    # Various ASCII chars have a special meaning for the operating system,
    # so make them more common
    ascii_char = characters(min_codepoint=0x01, max_codepoint=0x7f)
    if os.name == 'nt':  # pragma: no cover
        # Windows paths can contain all surrogates and even surrogate pairs
        # if two paths are concatenated. This makes it more likely for them to
        # be generated.
        surrogate = characters(
            min_codepoint=0xD800, max_codepoint=0xDFFF)
        uni_char = characters(min_codepoint=0x1)
        text_strategy = text(
            alphabet=one_of(uni_char, surrogate, ascii_char))

        def text_to_bytes(path):
            fs_enc = sys.getfilesystemencoding()
            try:
                return path.encode(fs_enc, 'surrogatepass')
            except UnicodeEncodeError:
                return path.encode(fs_enc, 'replace')

        bytes_strategy = text_strategy.map(text_to_bytes)
    else:
        latin_char = characters(min_codepoint=0x01, max_codepoint=0xff)
        bytes_strategy = text(alphabet=one_of(latin_char, ascii_char)).map(
            lambda t: t.encode('latin-1'))

        unix_path_text = bytes_strategy.map(
            lambda b: b.decode(
                sys.getfilesystemencoding(),
                'surrogateescape' if PY3 else 'ignore'))

        # Two surrogates generated through surrogateescape can generate
        # a valid utf-8 sequence when encoded and result in a different
        # code point when decoded again. Can happen when two paths get
        # concatenated. Shuffling makes it possible to generate such a case.
        text_strategy = permutations(draw(unix_path_text)).map(u"".join)

    if result_type is None:
        return draw(one_of(bytes_strategy, text_strategy))
    elif result_type is bytes:
        return draw(bytes_strategy)
    else:
        return draw(text_strategy)