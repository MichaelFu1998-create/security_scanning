def disconnect(self):
        """Disconnect from all databases"""
        for name, connection in self.items():
            if not connection.is_closed():
                connection.close()