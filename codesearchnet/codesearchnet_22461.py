def _camelcase_to_underscore(url):
    """
    Translate camelCase into underscore format.

    >>> _camelcase_to_underscore('minutesBetweenSummaries')
    'minutes_between_summaries'

    """
    def upper2underscore(text):
        for char in text:
            if char.islower():
                yield char
            else:
                yield '_'
                if char.isalpha():
                    yield char.lower()
    return ''.join(upper2underscore(url))