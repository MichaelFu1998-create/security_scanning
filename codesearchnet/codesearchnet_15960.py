def get_shark_field(self, fields):
        """get parameters via wireshark syntax.
        out = x.get_shark_field('wlan.fc.type')
        out = x.get_shark_field(['wlan.fc.type', 'wlan.seq'])
        :fields: str or str[]
        :return: dict
            out[fields[0]] = val[0] or None
            out[fields[1]] = val[1] or None ...
        """
        keys, exist, out = None, {}, None

        if isinstance(fields, str):
            fields = [fields]
        elif not isinstance(fields, list):
            logging.error('invalid input type')
            return None

        out = dict.fromkeys(fields)

        if hasattr(self, '_shark_'):
            exist.update(self._shark_)

        if hasattr(self, '_s_shark_'):
            exist.update(self._s_shark_)

        if hasattr(self.radiotap, '_r_shark_'):
            exist.update(self.radiotap._r_shark_)

        keys = exist.keys()

        for elem in fields:
            if elem in keys:
                obj_field, tmp = exist[elem], None
                try:
                    tmp = operator.attrgetter(obj_field)(self)
                except AttributeError:
                    tmp = None
                if not tmp:
                    try:
                        tmp = operator.attrgetter(obj_field)(self.radiotap)
                    except AttributeError:
                        tmp = None
                out[elem] = tmp
        return out