def _cut_range(self, line, start, current_position):
        """Performs cut for range from start position to end

        Arguments:
            line -              input to cut
            start -             start of range
            current_position -  current position in main cut function
        """
        result = []
        try:
            for j in range(start, len(line)):
                index = _setup_index(j)
                try:
                    result.append(line[index])
                except IndexError:
                    result.append(self.invalid_pos)
                finally:
                    result.append(self.separator)
            result.append(line[-1])
        except IndexError:
            pass

        try:
            int(self.positions[current_position+1])
            result.append(self.separator)
        except (ValueError, IndexError):
            pass

        return result