def render(self, only_line=False, colored=False):
        """
        Returns the human-readable location of the diagnostic in the source,
        the formatted message, the source line corresponding
        to ``location`` and a line emphasizing the problematic
        locations in the source line using ASCII art, as a list of lines.
        Appends the result of calling :meth:`render` on ``notes``, if any.

        For example: ::

            <input>:1:8-9: error: cannot add integer and string
            x + (1 + "a")
                 ~ ^ ~~~

        :param only_line: (bool) If true, only print line number, not line and column range
        """
        source_line = self.location.source_line().rstrip("\n")
        highlight_line = bytearray(re.sub(r"[^\t]", " ", source_line), "utf-8")

        for hilight in self.highlights:
            if hilight.line() == self.location.line():
                lft, rgt = hilight.column_range()
                highlight_line[lft:rgt] = bytearray("~", "utf-8") * (rgt - lft)

        lft, rgt = self.location.column_range()
        if rgt == lft: # Expand zero-length ranges to one ^
            rgt = lft + 1
        highlight_line[lft:rgt] = bytearray("^", "utf-8") * (rgt - lft)

        if only_line:
            location = "%s:%s" % (self.location.source_buffer.name, self.location.line())
        else:
            location = str(self.location)

        notes = list(self.notes)
        if self.level != "note":
            expanded_location = self.location.expanded_from
            while expanded_location is not None:
                notes.insert(0, Diagnostic("note",
                    "expanded from here", {},
                    self.location.expanded_from))
                expanded_location = expanded_location.expanded_from

        rendered_notes = reduce(list.__add__, [note.render(only_line, colored)
                                               for note in notes], [])
        if colored:
            if self.level in ("error", "fatal"):
                level_color = 31 # red
            elif self.level == "warning":
                level_color = 35 # magenta
            else: # level == "note"
                level_color = 30 # gray
            return [
                "\x1b[1;37m{}: \x1b[{}m{}:\x1b[37m {}\x1b[0m".
                    format(location, level_color, self.level, self.message()),
                source_line,
                "\x1b[1;32m{}\x1b[0m".format(highlight_line.decode("utf-8"))
            ] + rendered_notes
        else:
            return [
                "{}: {}: {}".format(location, self.level, self.message()),
                source_line,
                highlight_line.decode("utf-8")
            ] + rendered_notes