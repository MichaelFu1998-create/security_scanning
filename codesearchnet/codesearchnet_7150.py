def from_participantid(participant_id):
    """Convert hangouts_pb2.ParticipantId to UserID."""
    return user.UserID(
        chat_id=participant_id.chat_id,
        gaia_id=participant_id.gaia_id
    )