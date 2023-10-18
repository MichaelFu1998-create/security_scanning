def is_publication_permissible(cursor, publication_id, uuid_):
    """Check the given publisher of this publication given
    by ``publication_id`` is allowed to publish the content given
    by ``uuid``.
    """
    # Check the publishing user has permission to publish
    cursor.execute("""\
SELECT 't'::boolean
FROM
  pending_documents AS pd
  NATURAL JOIN document_acl AS acl
  JOIN publications AS p ON (pd.publication_id = p.id)
WHERE
  p.id = %s
  AND
  pd.uuid = %s
  AND
  p.publisher = acl.user_id
  AND
  acl.permission = 'publish'""", (publication_id, uuid_,))
    try:
        is_allowed = cursor.fetchone()[0]
    except TypeError:
        is_allowed = False
    return is_allowed