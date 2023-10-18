def __consonants_and_vowels(input_string):
    """__consonants_and_vowels(input_string) -> (string, list)

    Get the consonants as a string and the vowels as a list.
    """
    input_string = input_string.upper().replace(' ', '')

    consonants = [ char for char in input_string if char in __CONSONANTS ]
    vowels     = [ char for char in input_string if char in __VOWELS ]

    return "".join(consonants), vowels