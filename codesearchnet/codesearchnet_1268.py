def _columnNameDBToPublic(self, dbName):
    """ Convert a database internal column name to a public name. This
    takes something of the form word1_word2_word3 and converts it to:
    word1Word2Word3. If the db field name starts with '_', it is stripped out
    so that the name is compatible with collections.namedtuple.
    for example: _word1_word2_word3 => word1Word2Word3

    Parameters:
    --------------------------------------------------------------
    dbName:      database internal field name
    retval:      public name
    """

    words = dbName.split('_')
    if dbName.startswith('_'):
      words = words[1:]
    pubWords = [words[0]]
    for word in words[1:]:
      pubWords.append(word[0].upper() + word[1:])

    return ''.join(pubWords)