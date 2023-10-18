def _setup():
    """Add a variety of default schemes."""
    s = str.split
    if sys.version_info < (3, 0):
        # noinspection PyUnresolvedReferences
        s = unicode.split

    def pop_all(some_dict, some_list):
        for scheme in some_list:
            some_dict.pop(scheme)
    global SCHEMES
    SCHEMES = copy.deepcopy(sanscript.SCHEMES)
    pop_all(SCHEMES, [sanscript.ORIYA, sanscript.BENGALI, sanscript.GUJARATI])
    SCHEMES[HK].update({
        'vowels': s("""a A i I u U R RR lR lRR E ai O au""") + s("""e o"""),
        'marks': s("""A i I u U R RR lR lRR E ai O au""") + s("""e o"""),
        'consonants': sanscript.SCHEMES[HK]['consonants'] + s("""n2 r2 zh""")
    })
    SCHEMES[ITRANS].update({
        'vowels': s("""a A i I u U R RR LLi LLI E ai O au""") + s("""e o"""),
        'marks': s("""A i I u U R RR LLi LLI E ai O au""") + s("""e o"""),
        'consonants': sanscript.SCHEMES[ITRANS]['consonants'] + s("""n2 r2 zh""")
    })
    pop_all(SCHEMES[ITRANS].synonym_map, s("""e o"""))
    SCHEMES[OPTITRANS].update({
        'vowels': s("""a A i I u U R RR LLi LLI E ai O au""") + s("""e o"""),
        'marks': s("""A i I u U R RR LLi LLI E ai O au""") + s("""e o"""),
        'consonants': sanscript.SCHEMES[OPTITRANS]['consonants'] + s("""n2 r2 zh""")
    })
    pop_all(SCHEMES[OPTITRANS].synonym_map, s("""e o"""))