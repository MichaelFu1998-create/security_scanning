def default(self, obj):
        """Encode values as JSON strings.

        This method overrides the default implementation from
        `json.JSONEncoder`.
        """
        if isinstance(obj, datetime.datetime):
            return self._encode_datetime(obj)

        # Fallback to the default encoding
        return json.JSONEncoder.default(self, obj)