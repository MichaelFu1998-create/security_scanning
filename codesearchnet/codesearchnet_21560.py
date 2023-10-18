def exceptions(self):
        """A dict of dates -> [Period time tuples] representing exceptions
        to the base recurrence pattern."""
        ex = {}
        for sd in self.root.xpath('exceptions/exception'):
            bits = str(sd.text).split(' ')
            date = text_to_date(bits.pop(0))
            ex.setdefault(date, []).extend([
                _time_text_to_period(t)
                for t in bits
            ])
        return ex