def find_matches(strings, words, length_hoped):
        """ Used by default property excerpt """
        lower_words = [w.lower() for w in words]

        def has_match(string):
            """ Do any of the words match within the string """
            lower_string = string.lower()
            for test_word in lower_words:
                if test_word in lower_string:
                    return True
            return False

        shortened_strings = [textwrap.wrap(s) for s in strings]
        short_string_list = list(chain.from_iterable(shortened_strings))
        matches = [ms for ms in short_string_list if has_match(ms)]

        cumulative_len = 0
        break_at = None
        for idx, match in enumerate(matches):
            cumulative_len += len(match)
            if cumulative_len >= length_hoped:
                break_at = idx
                break

        return matches[0:break_at]