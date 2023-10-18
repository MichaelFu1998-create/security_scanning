def _fill_text(self, text, width, indent):
        """Overridden to not get rid of newlines

        https://github.com/python/cpython/blob/2.7/Lib/argparse.py#L620"""
        lines = []
        for line in text.splitlines(False):
            if line:
                # https://docs.python.org/2/library/textwrap.html
                lines.extend(textwrap.wrap(
                    line.strip(),
                    width,
                    initial_indent=indent,
                    subsequent_indent=indent
                ))

            else:
                lines.append(line)

        text = "\n".join(lines)
        return text