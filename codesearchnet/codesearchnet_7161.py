async def build_user_conversation_list(client):
    """Build :class:`.UserList` and :class:`.ConversationList`.

    This method requests data necessary to build the list of conversations and
    users. Users that are not in the contact list but are participating in a
    conversation will also be retrieved.

    Args:
        client (Client): Connected client.

    Returns:
        (:class:`.UserList`, :class:`.ConversationList`):
            Tuple of built objects.
    """
    conv_states, sync_timestamp = await _sync_all_conversations(client)

    # Retrieve entities participating in all conversations.
    required_user_ids = set()
    for conv_state in conv_states:
        required_user_ids |= {
            user.UserID(chat_id=part.id.chat_id, gaia_id=part.id.gaia_id)
            for part in conv_state.conversation.participant_data
        }
    required_entities = []
    if required_user_ids:
        logger.debug('Need to request additional users: {}'
                     .format(required_user_ids))
        try:
            response = await client.get_entity_by_id(
                hangouts_pb2.GetEntityByIdRequest(
                    request_header=client.get_request_header(),
                    batch_lookup_spec=[
                        hangouts_pb2.EntityLookupSpec(
                            gaia_id=user_id.gaia_id,
                            create_offnetwork_gaia=True,
                        )
                        for user_id in required_user_ids
                    ],
                )
            )
            for entity_result in response.entity_result:
                required_entities.extend(entity_result.entity)
        except exceptions.NetworkError as e:
            logger.warning('Failed to request missing users: {}'.format(e))

    # Build list of conversation participants.
    conv_part_list = []
    for conv_state in conv_states:
        conv_part_list.extend(conv_state.conversation.participant_data)

    # Retrieve self entity.
    get_self_info_response = await client.get_self_info(
        hangouts_pb2.GetSelfInfoRequest(
            request_header=client.get_request_header(),
        )
    )
    self_entity = get_self_info_response.self_entity

    user_list = user.UserList(client, self_entity, required_entities,
                              conv_part_list)
    conversation_list = ConversationList(client, conv_states,
                                         user_list, sync_timestamp)
    return (user_list, conversation_list)