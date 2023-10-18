def weekdays(self):
        """A set of integers representing the weekdays the schedule recurs on,
        with Monday = 0 and Sunday = 6."""
        if not self.root.xpath('days'):
            return set(range(7))
        return set(int(d) - 1 for d in self.root.xpath('days/day/text()'))