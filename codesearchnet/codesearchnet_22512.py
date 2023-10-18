def create_item(self, hash_key, start=0, extra_attrs=None):
        '''
        Hook point for overriding how the CouterPool creates a DynamoDB item
        for a given counter when an existing item can't be found.
        '''
        table = self.get_table()
        now = datetime.utcnow().replace(microsecond=0).isoformat()
        attrs = {
            'created_on': now,
            'modified_on': now,
            'count': start,
        }

        if extra_attrs:
            attrs.update(extra_attrs)

        item = table.new_item(
            hash_key=hash_key,
            attrs=attrs,
        )

        return item