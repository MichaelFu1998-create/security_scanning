def _on_event(self, conv_event):
        """Open conversation tab for new messages & pass events to notifier."""
        conv = self._conv_list.get(conv_event.conversation_id)
        user = conv.get_user(conv_event.user_id)
        show_notification = all((
            isinstance(conv_event, hangups.ChatMessageEvent),
            not user.is_self,
            not conv.is_quiet,
        ))
        if show_notification:
            self.add_conversation_tab(conv_event.conversation_id)
            if self._discreet_notifications:
                notification = DISCREET_NOTIFICATION
            else:
                notification = notifier.Notification(
                    user.full_name, get_conv_name(conv), conv_event.text
                )
            self._notifier.send(notification)