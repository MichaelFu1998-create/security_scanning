def from_conversation_event(conversation, conv_event, prev_conv_event,
                                datetimefmt, watermark_users=None):
        """Return MessageWidget representing a ConversationEvent.

        Returns None if the ConversationEvent does not have a widget
        representation.
        """
        user = conversation.get_user(conv_event.user_id)
        # Check whether the previous event occurred on the same day as this
        # event.
        if prev_conv_event is not None:
            is_new_day = (conv_event.timestamp.astimezone(tz=None).date() !=
                          prev_conv_event.timestamp.astimezone(tz=None).date())
        else:
            is_new_day = False
        if isinstance(conv_event, hangups.ChatMessageEvent):
            return MessageWidget(conv_event.timestamp, conv_event.text,
                                 datetimefmt, user, show_date=is_new_day,
                                 watermark_users=watermark_users)
        elif isinstance(conv_event, hangups.RenameEvent):
            if conv_event.new_name == '':
                text = ('{} cleared the conversation name'
                        .format(user.first_name))
            else:
                text = ('{} renamed the conversation to {}'
                        .format(user.first_name, conv_event.new_name))
            return MessageWidget(conv_event.timestamp, text, datetimefmt,
                                 show_date=is_new_day,
                                 watermark_users=watermark_users)
        elif isinstance(conv_event, hangups.MembershipChangeEvent):
            event_users = [conversation.get_user(user_id) for user_id
                           in conv_event.participant_ids]
            names = ', '.join([user.full_name for user in event_users])
            if conv_event.type_ == hangups.MEMBERSHIP_CHANGE_TYPE_JOIN:
                text = ('{} added {} to the conversation'
                        .format(user.first_name, names))
            else:  # LEAVE
                text = ('{} left the conversation'.format(names))
            return MessageWidget(conv_event.timestamp, text, datetimefmt,
                                 show_date=is_new_day,
                                 watermark_users=watermark_users)
        elif isinstance(conv_event, hangups.HangoutEvent):
            text = {
                hangups.HANGOUT_EVENT_TYPE_START: (
                    'A Hangout call is starting.'
                ),
                hangups.HANGOUT_EVENT_TYPE_END: (
                    'A Hangout call ended.'
                ),
                hangups.HANGOUT_EVENT_TYPE_ONGOING: (
                    'A Hangout call is ongoing.'
                ),
            }.get(conv_event.event_type, 'Unknown Hangout call event.')
            return MessageWidget(conv_event.timestamp, text, datetimefmt,
                                 show_date=is_new_day,
                                 watermark_users=watermark_users)
        elif isinstance(conv_event, hangups.GroupLinkSharingModificationEvent):
            status_on = hangups.GROUP_LINK_SHARING_STATUS_ON
            status_text = ('on' if conv_event.new_status == status_on
                           else 'off')
            text = '{} turned {} joining by link.'.format(user.first_name,
                                                          status_text)
            return MessageWidget(conv_event.timestamp, text, datetimefmt,
                                 show_date=is_new_day,
                                 watermark_users=watermark_users)
        else:
            # conv_event is a generic hangups.ConversationEvent.
            text = 'Unknown conversation event'
            return MessageWidget(conv_event.timestamp, text, datetimefmt,
                                 show_date=is_new_day,
                                 watermark_users=watermark_users)