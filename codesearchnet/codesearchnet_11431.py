def decorate_matches(match_in, match_word):
        """ decorate the matches within the excerpt """
        matches = re.finditer(match_word, match_in, re.IGNORECASE)
        for matched_string in set([match.group() for match in matches]):
            match_in = match_in.replace(
                matched_string,
                getattr(settings, "SEARCH_MATCH_DECORATION", u"<b>{}</b>").format(matched_string)
            )
        return match_in