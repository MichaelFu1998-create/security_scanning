def description(self):
        """A user-friendly description of the handler.

        Returns:
          :py:class:`str`: The handler's description.

        """
        if self._description is None:
            text = '\n'.join(self.__doc__.splitlines()[1:]).strip()
            lines = []
            for line in map(str.strip, text.splitlines()):
                if line and lines:
                    lines[-1] = ' '.join((lines[-1], line))
                elif line:
                    lines.append(line)
                else:
                    lines.append('')
            self._description = '\n'.join(lines)
        return self._description