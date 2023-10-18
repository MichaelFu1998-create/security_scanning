def to_participantid(user_id):
    """Convert UserID to hangouts_pb2.ParticipantId."""
    return hangouts_pb2.ParticipantId(
        chat_id=user_id.chat_id,
        gaia_id=user_id.gaia_id
    )