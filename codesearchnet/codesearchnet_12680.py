def parse_int_list(string):
    """
    Parses a string of numbers and ranges into a list of integers. Ranges
    are separated by dashes and inclusive of both the start and end number.

    Example:
        parse_int_list("8 9 10,11-13") == [8,9,10,11,12,13]
    """
    integers = []
    for comma_part in string.split(","):
        for substring in comma_part.split(" "):
            if len(substring) == 0:
                continue
            if "-" in substring:
                left, right = substring.split("-")
                left_val = int(left.strip())
                right_val = int(right.strip())
                integers.extend(range(left_val, right_val + 1))
            else:
                integers.append(int(substring.strip()))
    return integers