def parse(s):
        """
        Parses a string into a Tag
        """
        try:
            m = _regex.match(s)
            t = Tag(int(m.group('major')),
                    int(m.group('minor')),
                    int(m.group('patch')))
            return t \
                    if m.group('label') is None \
                    else t.with_revision(m.group('label'), int(m.group('number')))
        except AttributeError:
            return None