def get_random_name(retry=False):
    """
    generates a random name from the list of adjectives and birds in this package
    formatted as "adjective_surname". For example 'loving_sugarbird'. If retry is non-zero, a random
    integer between 0 and 100 will be added to the end of the name, e.g `loving_sugarbird3`
    """
    name = "%s_%s" % (left[random.randint(0, len(left) - 1)], right[random.randint(0, len(right) - 1)])
    if retry is True:
        name = "%s%d" % (name, random.randint(0, 100))
    return name