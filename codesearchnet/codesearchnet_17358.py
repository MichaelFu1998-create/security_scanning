def _glob_match(self, pattern, string):
        """
        Match given string, by escaping regex characters
        """
        # regex flags Multi-line, Unicode, Locale
        return bool(re.match(fnmatch.translate(pattern), string,
                             re.M | re.U | re.L))