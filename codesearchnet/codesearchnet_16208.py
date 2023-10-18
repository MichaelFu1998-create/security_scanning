def from_object(cls, obj):
        """The factory method to create WebDriverResult from JSON Object.

        Args:
            obj(dict): The JSON Object returned by server.
        """
        return cls(
            obj.get('sessionId', None),
            obj.get('status', 0),
            obj.get('value', None)
        )