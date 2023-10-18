def modify(self, setting, value):
        """Modify an already existing object.

        Positional argument SETTING is the setting name and VALUE is its value,
        which can be provided directly or obtained from a file name if prefixed with '@'.

        =====API DOCS=====
        Modify an already existing Tower setting.

        :param setting: The name of the Tower setting to be modified.
        :type setting: str
        :param value: The new value of the Tower setting.
        :type value: str
        :returns: A dictionary combining the JSON output of the modified resource, as well as two extra fields:
                  "changed", a flag indicating if the resource is successfully updated; "id", an integer which
                  is the primary key of the updated object.
        :rtype: dict

        =====API DOCS=====
        """
        prev_value = new_value = self.get(setting)['value']
        answer = OrderedDict()
        encrypted = '$encrypted$' in six.text_type(prev_value)

        if encrypted or six.text_type(prev_value) != six.text_type(value):
            if setting == 'LICENSE':
                r = client.post('/config/',
                                data=self.coerce_type(setting, value))
                new_value = r.json()
            else:
                r = client.patch(
                    self.endpoint,
                    data={setting: self.coerce_type(setting, value)}
                )
                new_value = r.json()[setting]
            answer.update(r.json())

        changed = encrypted or (prev_value != new_value)

        answer.update({
            'changed': changed,
            'id': setting,
            'value': new_value,
        })
        return answer