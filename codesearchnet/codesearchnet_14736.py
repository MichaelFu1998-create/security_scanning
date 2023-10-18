def __surname_triplet(input_string):
    """__surname_triplet(input_string) -> string"""
    consonants, vowels = __consonants_and_vowels(input_string)

    return __common_triplet(input_string, consonants, vowels)