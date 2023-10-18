def get_chat_id(self, message):
        '''
        Telegram chat type can be either "private", "group", "supergroup" or
        "channel".
        Return user ID if it is of type "private", chat ID otherwise.
        '''
        if message.chat.type == 'private':
            return message.user.id

        return message.chat.id