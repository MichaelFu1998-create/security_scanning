def get_accept_license(request):
    """This produces JSON data for a user (at ``uid``) to view the license(s)
    they have accepted or will need to accept for a publication (at ``id``).
    """
    publication_id = request.matchdict['id']
    user_id = request.matchdict['uid']

    # FIXME Is this an active publication?
    # TODO Verify the accepting user is the one making the request.

    # For each pending document, accept the license.
    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute("""
SELECT row_to_json(combined_rows) FROM (
SELECT
  pd.uuid AS id,
  ident_hash(pd.uuid, pd.major_version, pd.minor_version) \
    AS ident_hash,
  accepted AS is_accepted
FROM
  pending_documents AS pd
  NATURAL JOIN license_acceptances AS la
WHERE pd.publication_id = %s AND user_id = %s
) as combined_rows;""",
                           (publication_id, user_id))
            user_documents = [r[0] for r in cursor.fetchall()]

    return {'publication_id': publication_id,
            'user_id': user_id,
            'documents': user_documents,
            }