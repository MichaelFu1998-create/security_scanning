def _update_pending_document_state(cursor, document_id, is_license_accepted,
                                   are_roles_accepted):
    """Update the state of the document's state values."""
    args = (bool(is_license_accepted), bool(are_roles_accepted),
            document_id,)
    cursor.execute("""\
UPDATE pending_documents
SET (license_accepted, roles_accepted) = (%s, %s)
WHERE id = %s""",
                   args)