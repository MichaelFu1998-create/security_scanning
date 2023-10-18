def get_md_status(self, line):
        """Return a dict of md status define in the line."""
        ret = {}

        splitted = split('\W+', line)
        if len(splitted) < 7:
            ret['available'] = None
            ret['used'] = None
            ret['config'] = None
        else:
            # The final 2 entries on this line: [n/m] [UUUU_]
            # [n/m] means that ideally the array would have n devices however, currently, m devices are in use.
            # Obviously when m >= n then things are good.
            ret['available'] = splitted[-4]
            ret['used'] = splitted[-3]
            # [UUUU_] represents the status of each device, either U for up or _ for down.
            ret['config'] = splitted[-2]

        return ret