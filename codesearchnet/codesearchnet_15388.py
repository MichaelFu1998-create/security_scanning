def _check_pending_document_license_state(cursor, document_id):
    """Check the aggregate state on the pending document."""
    cursor.execute("""\
SELECT BOOL_AND(accepted IS TRUE)
FROM
  pending_documents AS pd,
  license_acceptances AS la
WHERE
  pd.id = %s
  AND
  pd.uuid = la.uuid""",
                   (document_id,))
    try:
        is_accepted = cursor.fetchone()[0]
    except TypeError:
        # There are no licenses associated with this document.
        is_accepted = True
    return is_accepted