def __common_triplet(input_string, consonants, vowels):
    """__common_triplet(input_string, consonants, vowels) -> string"""
    output = consonants

    while len(output) < 3:
        try:
            output += vowels.pop(0)
        except IndexError:
            # If there are less wovels than needed to fill the triplet,
            # (e.g. for a surname as "Fo'" or "Hu" or the corean "Y")
            # fill it with 'X';
            output += 'X'

    return output[:3]