def _setup_positions(self, positions):
        """Processes positions to account for ranges

        Arguments:
            positions -     list of positions and/or ranges to process
        """
        updated_positions = []

        for i, position in enumerate(positions):
            ranger = re.search(r'(?P<start>-?\d*):(?P<end>\d*)', position)

            if ranger:
                if i > 0:
                    updated_positions.append(self.separator)
                start = group_val(ranger.group('start'))
                end = group_val(ranger.group('end'))

                if start and end:
                    updated_positions.extend(self._extendrange(start, end + 1))
                # Since the number of positions on a line is unknown,
                # send input to cause exception that can be caught and call
                # _cut_range helper function
                elif ranger.group('start'):
                    updated_positions.append([start])
                else:
                    updated_positions.extend(self._extendrange(1, end + 1))
            else:
                updated_positions.append(positions[i])
                try:
                    if int(position) and int(positions[i+1]):
                        updated_positions.append(self.separator)
                except (ValueError, IndexError):
                    pass

        return updated_positions