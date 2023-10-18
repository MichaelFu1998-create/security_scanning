def from_json_list(cls, api_client, data):
        """Convert a list of JSON values to a list of models
        """
        return [cls.from_json(api_client, item) for item in data]