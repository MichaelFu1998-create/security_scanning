def build_message(self, data):
        '''
        Return a Message instance according to the data received from
        Telegram API.
        https://core.telegram.org/bots/api#update
        '''
        message_data = data.get('message') or data.get('edited_message')

        if not message_data:
            return None

        edited = 'edited_message' in data
        return Message(
            id=message_data['message_id'],
            platform=self.platform,
            text=message_data.get('text', ''),
            user=TelegramUser(message_data['from']),
            chat=TelegramChat(message_data['chat']),
            timestamp=message_data['date'],
            raw=data,
            edited=edited,
        )