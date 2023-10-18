def replace_entities(ustring, placeholder=" "):

    """Replaces HTML special characters by readable characters.

    As taken from Leif K-Brooks algorithm on:
    http://groups-beta.google.com/group/comp.lang.python
    
    """

    def _repl_func(match):
        try:
            if match.group(1): # Numeric character reference
                return unichr( int(match.group(2)) ) 
            else:
                try: return cp1252[ unichr(int(match.group(3))) ].strip()
                except: return unichr( name2codepoint[match.group(3)] )
        except:
            return placeholder

    # Force to Unicode.
    if not isinstance(ustring, unicode):
        ustring = UnicodeDammit(ustring).unicode
    
    # Don't want some weird unicode character here
    # that truncate_spaces() doesn't know of:
    ustring = ustring.replace("&nbsp;", " ")
    
    # The ^> makes sure nothing inside a tag (i.e. href with query arguments) gets processed.
    _entity_re = re.compile(r'&(?:(#)(\d+)|([^;^> ]+));') 
    return _entity_re.sub(_repl_func, ustring)