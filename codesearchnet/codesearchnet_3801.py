def _format_id(self, payload):
        """Echos only the id"""
        if 'id' in payload:
            return str(payload['id'])
        if 'results' in payload:
            return ' '.join([six.text_type(item['id']) for item in payload['results']])
        raise MultipleRelatedError('Could not serialize output with id format.')