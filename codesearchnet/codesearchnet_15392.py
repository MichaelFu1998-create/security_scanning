def poke_publication_state(publication_id, cursor):
    """Invoked to poke at the publication to update and acquire its current
    state. This is used to persist the publication to archive.
    """
    cursor.execute("""\
SELECT "state", "state_messages", "is_pre_publication", "publisher"
FROM publications
WHERE id = %s""", (publication_id,))
    row = cursor.fetchone()
    current_state, messages, is_pre_publication, publisher = row

    if current_state in END_N_INTERIM_STATES:
        # Bailout early, because the publication is either in progress
        # or has been completed.
        return current_state, messages

    # Check for acceptance...
    cursor.execute("""\
SELECT
  pd.id, license_accepted, roles_accepted
FROM publications AS p JOIN pending_documents AS pd ON p.id = pd.publication_id
WHERE p.id = %s
""", (publication_id,))
    pending_document_states = cursor.fetchall()
    publication_state_mapping = {}
    for document_state in pending_document_states:
        id, is_license_accepted, are_roles_accepted = document_state
        publication_state_mapping[id] = [is_license_accepted,
                                         are_roles_accepted]
        has_changed_state = False
        if is_license_accepted and are_roles_accepted:
            continue
        if not is_license_accepted:
            accepted = _check_pending_document_license_state(
                cursor, id)
            if accepted != is_license_accepted:
                has_changed_state = True
                is_license_accepted = accepted
                publication_state_mapping[id][0] = accepted
        if not are_roles_accepted:
            accepted = _check_pending_document_role_state(
                cursor, id)
            if accepted != are_roles_accepted:
                has_changed_state = True
                are_roles_accepted = accepted
                publication_state_mapping[id][1] = accepted
        if has_changed_state:
            _update_pending_document_state(cursor, id,
                                           is_license_accepted,
                                           are_roles_accepted)

    # Are all the documents ready for publication?
    state_lump = set([l and r for l, r in publication_state_mapping.values()])
    is_publish_ready = not (False in state_lump) and not (None in state_lump)
    change_state = "Done/Success"
    if not is_publish_ready:
        change_state = "Waiting for acceptance"

    # Does this publication need moderation? (ignore on pre-publication)
    # TODO Is this a revision publication? If so, it doesn't matter who the
    #      user is, because they have been vetted by the previous publisher.
    #      This has loopholes...
    if not is_pre_publication and is_publish_ready:
        # Has this publisher been moderated before?
        cursor.execute("""\
SELECT is_moderated
FROM users AS u LEFT JOIN publications AS p ON (u.username = p.publisher)
WHERE p.id = %s""",
                       (publication_id,))
        try:
            is_publisher_moderated = cursor.fetchone()[0]
        except TypeError:
            is_publisher_moderated = False

        # Are any of these documents a revision? Thus vetting of
        #   the publisher was done by a vetted peer.
        if not is_publisher_moderated \
           and not is_revision_publication(publication_id, cursor):
            # Hold up! This publish needs moderation.
            change_state = "Waiting for moderation"
            is_publish_ready = False

    # Publish the pending documents.
    if is_publish_ready:
        change_state = "Done/Success"
        if not is_pre_publication:
            publication_state = publish_pending(cursor, publication_id)
        else:
            cursor.execute("""\
UPDATE publications
SET state = %s
WHERE id = %s
RETURNING state, state_messages""", (change_state, publication_id,))
            publication_state, messages = cursor.fetchone()
    else:
        # `change_state` set prior to this...
        cursor.execute("""\
UPDATE publications
SET state = %s
WHERE id = %s
RETURNING state, state_messages""", (change_state, publication_id,))
        publication_state, messages = cursor.fetchone()

    return publication_state, messages