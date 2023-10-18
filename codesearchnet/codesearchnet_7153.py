def parse_watermark_notification(p):
    """Return WatermarkNotification from hangouts_pb2.WatermarkNotification."""
    return WatermarkNotification(
        conv_id=p.conversation_id.id,
        user_id=from_participantid(p.sender_id),
        read_timestamp=from_timestamp(
            p.latest_read_timestamp
        ),
    )