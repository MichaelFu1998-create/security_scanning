def accept_publication_license(cursor, publication_id, user_id,
                               document_ids, is_accepted=False):
    """Accept or deny  the document license for the publication
    (``publication_id``) and user (at ``user_id``)
    for the documents (listed by id as ``document_ids``).
    """
    cursor.execute("""\
UPDATE license_acceptances AS la
SET accepted = %s
FROM pending_documents AS pd
WHERE
  pd.publication_id = %s
  AND
  la.user_id = %s
  AND
  pd.uuid = ANY(%s::UUID[])
  AND
  pd.uuid = la.uuid""",
                   (is_accepted, publication_id, user_id, document_ids,))