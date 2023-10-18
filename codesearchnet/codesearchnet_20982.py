def render_vars(self):
        """Template variables."""
        return {
            'records': [
                {
                    'message': record.getMessage(),
                    'time': dt.datetime.fromtimestamp(record.created).strftime('%H:%M:%S'),
                } for record in self.handler.records
            ]
        }