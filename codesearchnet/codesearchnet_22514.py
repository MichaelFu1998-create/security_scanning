def get_counter(self, name, start=0):
        '''
        Gets the DynamoDB item behind a counter and ties it to a Counter
        instace.
        '''
        item = self.get_item(hash_key=name, start=start)
        counter = Counter(dynamo_item=item, pool=self)

        return counter