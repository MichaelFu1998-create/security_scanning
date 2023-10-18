def notify_users(cursor, document_id):
    """Notify all users about their role and/or license acceptance
    for a piece of content associated with the given ``document_id``.
    """
    return

    registry = get_current_registry()
    accounts = registry.getUtility(IOpenstaxAccounts)
    cursor.execute("""\
SELECT la.user_id
FROM license_acceptances AS la
WHERE
  la.uuid = (SELECT uuid FROM pending_documents WHERE id = %s)
  AND la.notified IS NULL AND (NOT la.accepted or la.accepted IS UNKNOWN)
""", (document_id,))
    licensors = [x[0] for x in cursor.fetchall()]

    cursor.execute("""\
SELECT user_id, array_agg(role_type)::text[]
FROM role_acceptances AS ra
WHERE
  ra.uuid = (SELECT uuid FROM pending_documents WHERE id = %s)
  AND ra.notified IS NULL AND (NOT ra.accepted or ra.accepted IS UNKNOWN)
GROUP BY user_id
""", (document_id,))
    roles = {u: r for u, r in cursor.fetchall()}

    needs_notified = set(licensors + roles.keys())

    for user_id in needs_notified:
        data = {
            'user_id': user_id,
            'full_name': None,  # TODO
            'licensor': user_id in licensors,
            'roles': roles.get(user_id, []),
        }
        message = NOTIFICATION_TEMPLATE.render(**data)
        accounts.send_message(user_id, NOFIFICATION_SUBJECT, message)

    cursor.execute("""\
UPDATE license_acceptances SET notified = CURRENT_TIMESTAMP
WHERE
  uuid = (SELECT uuid FROM pending_documents WHERE id = %s)
  AND user_id = ANY (%s)""", (document_id, licensors,))
    # FIXME overwrites notified for all roles types a user might have.
    cursor.execute("""\
UPDATE role_acceptances SET notified = CURRENT_TIMESTAMP
WHERE
  uuid = (SELECT uuid FROM pending_documents WHERE id = %s)
  AND user_id = ANY (%s)""", (document_id, roles.keys(),))