def accept_publication_role(cursor, publication_id, user_id,
                            document_ids, is_accepted=False):
    """Accept or deny  the document role attribution for the publication
    (``publication_id``) and user (at ``user_id``)
    for the documents (listed by id as ``document_ids``).
    """
    cursor.execute("""\
UPDATE role_acceptances AS ra
SET accepted = %s
FROM pending_documents AS pd
WHERE
  pd.publication_id = %s
  AND
  ra.user_id = %s
  AND
  pd.uuid = ANY(%s::UUID[])
  AND
  pd.uuid = ra.uuid""",
                   (is_accepted, publication_id, user_id, document_ids,))