def main(argv=None):
    """ Call transliterator from a command line.
    
    python transliterator.py text inputFormat outputFormat
    
    ... writes the transliterated text to stdout
    
    text -- the text to be transliterated OR the name of a file containing the text
    inputFormat -- the name of the character block or transliteration scheme that
                   the text is to be transliterated FROM, e.g. 'CYRILLIC', 'IAST'.
                   Not case-sensitive
    outputFormat -- the name of the character block or transliteration scheme that
                   the text is to be transliterated TO, e.g. 'CYRILLIC', 'IAST'.
                   Not case-sensitive
    
    """
    print (transliterate('jaya gaNeza! zrIrAmajayam', 'harvardkyoto', 'devanagari'))
    if argv is None:
        argv = sys.argv
    try:    
        text, inFormat, outFormat = argv[1:4]
    except ValueError:
        print (main.__doc__)
        return 2
    inFormat = inFormat.upper()
    outFormat = outFormat.upper()
    # try assuming "text" is a filename
    try:
        f = open(text)
    except IOError:
        # it wasn't, so it must be the actual text
        print (transliterate(text, inFormat, outFormat))
        return 0
    else:
        i = 1
        for text in f.readlines():
            if len(text) > 0 and not text.startswith('#'):
                print (transliterate(text, inFormat, outFormat).strip('\n'))
            i = i + 1
        f.close()
        return 0