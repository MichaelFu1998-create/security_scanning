def _generate_html_diff(self, expected_fn, expected_lines, obtained_fn, obtained_lines):
        """
        Returns a nice side-by-side diff of the given files, as a string.

        """
        import difflib
        differ = difflib.HtmlDiff()
        return differ.make_file(
            fromlines=expected_lines,
            fromdesc=expected_fn,
            tolines=obtained_lines,
            todesc=obtained_fn,
        )