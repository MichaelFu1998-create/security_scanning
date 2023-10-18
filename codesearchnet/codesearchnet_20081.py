def message_is_to_me(self, data):
        """If you send a message directly to me"""
        return (data.get('type') == 'message' and
                data.get('text', '').startswith(self.address_as))