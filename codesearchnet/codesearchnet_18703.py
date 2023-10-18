def fix_title_capitalization(title):
    """Try to capitalize properly a title string."""
    if re.search("[A-Z]", title) and re.search("[a-z]", title):
        return title
    word_list = re.split(' +', title)
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        if word.upper() in COMMON_ACRONYMS:
            final.append(word.upper())
        elif len(word) > 3:
            final.append(word.capitalize())
        else:
            final.append(word.lower())
    return " ".join(final)