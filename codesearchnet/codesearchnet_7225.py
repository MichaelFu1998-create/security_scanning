def _update(self):
        """Update status text."""
        typing_users = [self._conversation.get_user(user_id)
                        for user_id, status in self._typing_statuses.items()
                        if status == hangups.TYPING_TYPE_STARTED]
        displayed_names = [user.first_name for user in typing_users
                           if not user.is_self]
        if displayed_names:
            typing_message = '{} {} typing...'.format(
                ', '.join(sorted(displayed_names)),
                'is' if len(displayed_names) == 1 else 'are'
            )
        else:
            typing_message = ''

        if not self._is_connected:
            self._widget.set_text("RECONNECTING...")
        elif self._message is not None:
            self._widget.set_text(self._message)
        else:
            self._widget.set_text(typing_message)