def assert_match(actual_char_or_str, expected_char_or_str):
    """If values don't match, print them and raise a ValueError, otherwise,
    continue
    Raises: ValueError if argumetns do not match"""
    if expected_char_or_str != actual_char_or_str:
        print("Expected")
        pprint(expected_char_or_str)
        print("")
        print("Got")
        pprint(actual_char_or_str)
        raise ValueError()