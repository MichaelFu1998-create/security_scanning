def strings_in_dictionary(dictionary):
        """ Used by default implementation for finding excerpt """
        strings = [value for value in six.itervalues(dictionary) if not isinstance(value, dict)]
        for child_dict in [dv for dv in six.itervalues(dictionary) if isinstance(dv, dict)]:
            strings.extend(SearchResultProcessor.strings_in_dictionary(child_dict))
        return strings