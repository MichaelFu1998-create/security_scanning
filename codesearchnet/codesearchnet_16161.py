def build_message(self, data):
        '''
        Return a Message instance according to the data received from
        Facebook Messenger API.
        '''
        if not data:
            return None

        return Message(
            id=data['message']['mid'],
            platform=self.platform,
            text=data['message']['text'],
            user=data['sender']['id'],
            timestamp=data['timestamp'],
            raw=data,
            chat=None,  # TODO: Refactor build_messages and Message class
        )