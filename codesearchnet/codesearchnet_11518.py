def from_json(cls, api_client, data):
        """Convert one JSON value to a model object
        """
        self = cls(api_client)
        PandoraModel.populate_fields(api_client, self, data)
        return self