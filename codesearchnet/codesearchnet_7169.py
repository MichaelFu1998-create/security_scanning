def _wrap_event(event_):
        """Wrap hangouts_pb2.Event in ConversationEvent subclass."""
        cls = conversation_event.ConversationEvent
        if event_.HasField('chat_message'):
            cls = conversation_event.ChatMessageEvent
        elif event_.HasField('otr_modification'):
            cls = conversation_event.OTREvent
        elif event_.HasField('conversation_rename'):
            cls = conversation_event.RenameEvent
        elif event_.HasField('membership_change'):
            cls = conversation_event.MembershipChangeEvent
        elif event_.HasField('hangout_event'):
            cls = conversation_event.HangoutEvent
        elif event_.HasField('group_link_sharing_modification'):
            cls = conversation_event.GroupLinkSharingModificationEvent
        return cls(event_)