def generate_words(files):
    """
    Transform list of files to list of words,
    removing new line character
    and replace name entity '<NE>...</NE>' and abbreviation '<AB>...</AB>' symbol
    """

    repls = {'<NE>' : '','</NE>' : '','<AB>': '','</AB>': ''}

    words_all = []
    for i, file in enumerate(files):
        lines = open(file, 'r')
        for line in lines:
            line = reduce(lambda a, kv: a.replace(*kv), repls.items(), line)
            words = [word for word in line.split("|") if word is not '\n']
            words_all.extend(words)
    return words_all