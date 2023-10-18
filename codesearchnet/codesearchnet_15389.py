def _check_pending_document_role_state(cursor, document_id):
    """Check the aggregate state on the pending document."""
    cursor.execute("""\
SELECT BOOL_AND(accepted IS TRUE)
FROM
  role_acceptances AS ra,
  pending_documents as pd
WHERE
  pd.id = %s
  AND
  pd.uuid = ra.uuid""",
                   (document_id,))
    try:
        is_accepted = cursor.fetchone()[0]
    except TypeError:
        # There are no roles to accept
        is_accepted = True
    return is_accepted