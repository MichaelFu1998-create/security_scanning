def get(self, key_name):
        """Gets the key.
        :return: The key itself in a dictionary
        """
        try:
            obj = self.client.get_object(
                Bucket=self.db_path,
                Key=key_name)['Body'].read().decode("utf-8")

            return json.loads(obj)
        except botocore.exceptions.ClientError as e:
            if 'NoSuchKey' in str(e.response['Error']['Code']):
                return {}
            raise e