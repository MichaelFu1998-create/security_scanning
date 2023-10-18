def _update_dict(data, default_data, replace_data=False):
        '''Update algorithm definition type dictionaries'''

        if not data:
            data = default_data.copy()
            return data

        if not isinstance(data, dict):
            raise TypeError('Value not dict type')
        if len(data) > 255:
            raise ValueError('More than 255 values defined')
        for i in data.keys():
            if not isinstance(i, int):
                raise TypeError('Index not int type')
            if i < 0 or i > 255:
                raise ValueError('Index value out of range')

        if not replace_data:
            data.update(default_data)

        return data