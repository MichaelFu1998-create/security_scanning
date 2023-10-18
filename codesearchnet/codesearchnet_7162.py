async def _sync_all_conversations(client):
    """Sync all conversations by making paginated requests.

    Conversations are ordered by ascending sort timestamp.

    Args:
        client (Client): Connected client.

    Raises:
        NetworkError: If the requests fail.

    Returns:
        tuple of list of ``ConversationState`` messages and sync timestamp
    """
    conv_states = []
    sync_timestamp = None
    request = hangouts_pb2.SyncRecentConversationsRequest(
        request_header=client.get_request_header(),
        max_conversations=CONVERSATIONS_PER_REQUEST,
        max_events_per_conversation=1,
        sync_filter=[
            hangouts_pb2.SYNC_FILTER_INBOX,
            hangouts_pb2.SYNC_FILTER_ARCHIVED,
        ]
    )
    for _ in range(MAX_CONVERSATION_PAGES):
        logger.info(
            'Requesting conversations page %s', request.last_event_timestamp
        )
        response = await client.sync_recent_conversations(request)
        conv_states = list(response.conversation_state) + conv_states
        sync_timestamp = parsers.from_timestamp(
            # SyncRecentConversations seems to return a sync_timestamp 4
            # minutes before the present. To prevent SyncAllNewEvents later
            # breaking requesting events older than what we already have, use
            # current_server_time instead.
            response.response_header.current_server_time
        )
        if response.continuation_end_timestamp == 0:
            logger.info('Reached final conversations page')
            break
        else:
            request.last_event_timestamp = response.continuation_end_timestamp
    else:
        logger.warning('Exceeded maximum number of conversation pages')
    logger.info('Synced %s total conversations', len(conv_states))
    return conv_states, sync_timestamp