def save_value(self, key, value):
        """
        Save an arbitrary, serializable `value` under `key`.

        :param str key: A string identifier under which to store the value.
        :param value: A serializable value
        :return:
        """
        with self.save_stream(key) as s:
            s.write(value)