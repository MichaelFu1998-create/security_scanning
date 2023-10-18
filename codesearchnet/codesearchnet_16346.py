def adjust(self, to):
        '''
        Adjusts the time from kwargs to timedelta
        **Will change this object**

        return new copy of self
        '''
        if self.date == 'infinity':
            return
        new = copy(self)
        if type(to) in (str, unicode):
            to = to.lower()
            res = TIMESTRING_RE.search(to)
            if res:
                rgroup = res.groupdict()
                if (rgroup.get('delta') or rgroup.get('delta_2')):
                    i = int(text2num(rgroup.get('num', 'one'))) * (-1 if to.startswith('-') else 1)
                    delta = (rgroup.get('delta') or rgroup.get('delta_2')).lower()
                    if delta.startswith('y'):
                        try:
                            new.date = new.date.replace(year=(new.date.year + i))
                        except ValueError:
                            # day is out of range for month
                            new.date = new.date + timedelta(days=(365 * i))
                    elif delta.startswith('month'):
                        if (new.date.month + i) > 12:
                            new.date = new.date.replace(month=(i - (i / 12)),
                                                        year=(new.date.year + 1 + (i / 12)))
                        elif (new.date.month + i) < 1:
                            new.date = new.date.replace(month=12, year=(new.date.year - 1))
                        else:
                            new.date = new.date.replace(month=(new.date.month + i))
                    elif delta.startswith('q'):
                        # NP
                        pass
                    elif delta.startswith('w'):
                        new.date = new.date + timedelta(days=(7 * i))
                    elif delta.startswith('s'):
                        new.date = new.date + timedelta(seconds=i)
                    else:
                        new.date = new.date + timedelta(**{('days' if delta.startswith('d') else 'hours' if delta.startswith('h') else 'minutes' if delta.startswith('m') else 'seconds'): i})
                    return new
        else:
            new.date = new.date + timedelta(seconds=int(to))
            return new

        raise TimestringInvalid('Invalid addition request')