def get_conn(self, aws_access_key=None, aws_secret_key=None):
        '''
        Hook point for overriding how the CounterPool gets its connection to
        AWS.
        '''
        return boto.connect_dynamodb(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
        )