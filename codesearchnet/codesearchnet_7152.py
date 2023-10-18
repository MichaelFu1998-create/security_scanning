def parse_typing_status_message(p):
    """Return TypingStatusMessage from hangouts_pb2.SetTypingNotification.

    The same status may be sent multiple times consecutively, and when a
    message is sent the typing status will not change to stopped.
    """
    return TypingStatusMessage(
        conv_id=p.conversation_id.id,
        user_id=from_participantid(p.sender_id),
        timestamp=from_timestamp(p.timestamp),
        status=p.type,
    )