def __name_triplet(input_string):
    """__name_triplet(input_string) -> string"""
    if input_string == '':
        # highly unlikely: no first name, like for instance some Indian persons
        # with only one name on the passport
        # pylint: disable=W0511
        return 'XXX' 

    consonants, vowels = __consonants_and_vowels(input_string)
    
    if len(consonants) > 3:
        return "%s%s%s" % (consonants[0], consonants[2], consonants[3])

    return __common_triplet(input_string, consonants, vowels)