def tokenize(sentence):
    """
    Converts a single sentence into a list of individual significant units
    Args:
        sentence (str): Input string ie. 'This is a sentence.'
    Returns:
        list<str>: List of tokens ie. ['this', 'is', 'a', 'sentence']
    """
    tokens = []

    class Vars:
        start_pos = -1
        last_type = 'o'

    def update(c, i):
        if c.isalpha() or c in '-{}':
            t = 'a'
        elif c.isdigit() or c == '#':
            t = 'n'
        elif c.isspace():
            t = 's'
        else:
            t = 'o'

        if t != Vars.last_type or t == 'o':
            if Vars.start_pos >= 0:
                token = sentence[Vars.start_pos:i].lower()
                if token not in '.!?':
                    tokens.append(token)
            Vars.start_pos = -1 if t == 's' else i
        Vars.last_type = t

    for i, char in enumerate(sentence):
        update(char, i)
    update(' ', len(sentence))
    return tokens