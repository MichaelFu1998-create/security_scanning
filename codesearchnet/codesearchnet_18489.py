def camelize_classname(base, tablename, table):
    "Produce a 'camelized' class name, e.g. "
    "'words_and_underscores' -> 'WordsAndUnderscores'"
    return str(tablename[0].upper() +
               re.sub(r'_([a-z])', lambda m: m.group(1).upper(),
                      tablename[1:]))