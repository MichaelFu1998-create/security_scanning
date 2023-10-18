def post_license_request(request):
    """Submission to create a license acceptance request."""
    uuid_ = request.matchdict['uuid']

    posted_data = request.json
    license_url = posted_data.get('license_url')
    licensors = posted_data.get('licensors', [])
    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute("""\
SELECT l.url
FROM document_controls AS dc
LEFT JOIN licenses AS l ON (dc.licenseid = l.licenseid)
WHERE uuid = %s::UUID""", (uuid_,))
            try:
                # Check that the license exists
                existing_license_url = cursor.fetchone()[0]
            except TypeError:  # NoneType
                if request.has_permission('publish.create-identifier'):
                    cursor.execute("""\
INSERT INTO document_controls (uuid) VALUES (%s)""", (uuid_,))
                    existing_license_url = None
                else:
                    raise httpexceptions.HTTPNotFound()
            if existing_license_url is None and license_url is None:
                raise httpexceptions.HTTPBadRequest("license_url is required")
            elif (license_url != existing_license_url or
                  existing_license_url is None):
                cursor.execute("""\
UPDATE document_controls AS dc
SET licenseid = l.licenseid FROM licenses AS l
WHERE url = %s and is_valid_for_publication = 't'
RETURNING dc.licenseid""",
                               (license_url,))
                try:
                    # Check that it is a valid license id
                    cursor.fetchone()[0]
                except TypeError:  # None returned
                    raise httpexceptions.HTTPBadRequest("invalid license_url")
            upsert_license_requests(cursor, uuid_, licensors)

    resp = request.response
    resp.status_int = 202
    return resp