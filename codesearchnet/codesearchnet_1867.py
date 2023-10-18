def _qformat(self, aline, bline, atags, btags):
        r"""
        Format "?" output and deal with leading tabs.

        Example:

        >>> d = Differ()
        >>> results = d._qformat('\tabcDefghiJkl\n', '\tabcdefGhijkl\n',
        ...                      '  ^ ^  ^      ', '  ^ ^  ^      ')
        >>> for line in results: print repr(line)
        ...
        '- \tabcDefghiJkl\n'
        '? \t ^ ^  ^\n'
        '+ \tabcdefGhijkl\n'
        '? \t ^ ^  ^\n'
        """

        # Can hurt, but will probably help most of the time.
        common = min(_count_leading(aline, "\t"),
                     _count_leading(bline, "\t"))
        common = min(common, _count_leading(atags[:common], " "))
        common = min(common, _count_leading(btags[:common], " "))
        atags = atags[common:].rstrip()
        btags = btags[common:].rstrip()

        yield "- " + aline
        if atags:
            yield "? %s%s\n" % ("\t" * common, atags)

        yield "+ " + bline
        if btags:
            yield "? %s%s\n" % ("\t" * common, btags)