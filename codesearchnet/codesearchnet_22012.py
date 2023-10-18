def cut(self, line):
        """Returns selected positions from cut input source in desired
        arrangement.

        Argument:
            line -      input to cut
        """
        result = []
        line = self.line(line)

        for i, field in enumerate(self.positions):
            try:
                index = _setup_index(field)
                try:
                    result += line[index]
                except IndexError:
                    result.append(self.invalid_pos)
            except ValueError:
                result.append(str(field))
            except TypeError:
                result.extend(self._cut_range(line, int(field[0]), i))

        return ''.join(result)