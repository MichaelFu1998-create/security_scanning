def get_item(self, hash_key, start=0, extra_attrs=None):
        '''
        Hook point for overriding how the CouterPool fetches a DynamoDB item
        for a given counter.
        '''
        table = self.get_table()

        try:
            item = table.get_item(hash_key=hash_key)
        except DynamoDBKeyNotFoundError:
            item = None

        if item is None:
            item = self.create_item(
                hash_key=hash_key,
                start=start,
                extra_attrs=extra_attrs,
            )

        return item