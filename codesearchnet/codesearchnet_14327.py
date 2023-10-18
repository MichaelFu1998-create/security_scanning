def best_units(self, sequence):
        """
        Determine good units for representing a sequence of timedeltas
        """
        # Read
        #   [(0.9, 's'),
        #    (9, 'm)]
        # as, break ranges between 0.9 seconds (inclusive)
        # and 9 minutes are represented in seconds. And so on.
        ts_range = self.value(max(sequence)) - self.value(min(sequence))
        package = self.determine_package(sequence[0])
        if package == 'pandas':
            cuts = [
                (0.9, 'us'),
                (0.9, 'ms'),
                (0.9, 's'),
                (9, 'm'),
                (6, 'h'),
                (4, 'd'),
                (4, 'w'),
                (4, 'M'),
                (3, 'y')]
            denomination = NANOSECONDS
            base_units = 'ns'
        else:
            cuts = [
                (0.9, 's'),
                (9, 'm'),
                (6, 'h'),
                (4, 'd'),
                (4, 'w'),
                (4, 'M'),
                (3, 'y')]
            denomination = SECONDS
            base_units = 'ms'

        for size, units in reversed(cuts):
            if ts_range >= size*denomination[units]:
                return units

        return base_units