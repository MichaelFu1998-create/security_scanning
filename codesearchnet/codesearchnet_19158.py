def find_words(text, suspect_words, excluded_words=[]):
    """Check if a text has some of the suspect words (or words that starts with
    one of the suspect words). You can set some words to be excluded of the
    search, so you can remove false positives like 'important' be detected when
    you search by 'import'. It will return True if the number of suspect words
    found is greater than the number of excluded words. Otherwise, it will
    return False.

    Args:
        text (str): a string with the text to be analysed. It will be converted
            to lowercase.
        suspect_words: a list of strings that you want to check the presence in
            the text.
        excluded_words: a list of strings to be whitelisted.
    """
    text = text.lower()
    suspect_found = [i for i in re.finditer(make_regex(suspect_words), text)]
    if len(excluded_words) > 0:
        excluded_found = [i for i in re.finditer(make_regex(excluded_words), text)]
        if len(suspect_found) > len(excluded_found):
            return True
        else:
            return False
    else:
        if len(suspect_found) > 0:
            return True
        else:
            return False