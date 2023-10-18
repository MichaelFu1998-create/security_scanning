def add_pending_model(cursor, publication_id, model):
    """Adds a model (binder or document) that is awaiting publication
    to the database.
    """
    # FIXME Too much happening here...
    assert isinstance(model, (cnxepub.Document, cnxepub.Binder,)), type(model)
    uri = model.get_uri('cnx-archive')

    if uri is not None:
        ident_hash = parse_archive_uri(uri)
        id, version = split_ident_hash(ident_hash, split_version=True)
        cursor.execute("""\
SELECT major_version + 1 as next_version
FROM latest_modules
WHERE uuid = %s
UNION ALL
SELECT 1 as next_version
ORDER BY next_version DESC
LIMIT 1
""", (id,))
        next_major_version = cursor.fetchone()[0]
        if isinstance(model, cnxepub.Document):
            version = (next_major_version, None,)
        else:  # ...assume it's a binder.
            version = (next_major_version, 1,)
    else:
        cursor.execute("""\
WITH
control_insert AS (
  INSERT INTO document_controls (uuid) VALUES (DEFAULT) RETURNING uuid),
acl_insert AS (
  INSERT INTO document_acl (uuid, user_id, permission)
  VALUES ((SELECT uuid FROM control_insert),
          (SELECT publisher FROM publications WHERE id = %s),
          'publish'::permission_type))
SELECT uuid FROM control_insert""", (publication_id,))
        id = cursor.fetchone()[0]
        if isinstance(model, cnxepub.Document):
            version = (1, None,)
        else:  # ...assume it's a binder.
            version = (1, 1,)

    type_ = _get_type_name(model)
    model.id = str(id)
    model.metadata['version'] = '.'.join([str(v) for v in version if v])
    args = [publication_id, id, version[0], version[1], type_,
            json.dumps(model.metadata)]
    cursor.execute("""\
INSERT INTO "pending_documents"
  ("publication_id", "uuid", "major_version", "minor_version", "type",
    "license_accepted", "roles_accepted", "metadata")
VALUES (%s, %s, %s, %s, %s, 'f', 'f', %s)
RETURNING "id", "uuid", module_version("major_version", "minor_version")
""", args)
    pending_id, uuid_, version = cursor.fetchone()
    pending_ident_hash = join_ident_hash(uuid_, version)

    # Assign the new ident-hash to the document for later use.
    request = get_current_request()
    path = request.route_path('get-content', ident_hash=pending_ident_hash)
    model.set_uri('cnx-archive', path)

    # Check if the publication is allowed for the publishing user.
    if not is_publication_permissible(cursor, publication_id, id):
        # Set the failure but continue the operation of inserting
        # the pending document.
        exc = exceptions.NotAllowed(id)
        exc.publication_id = publication_id
        exc.pending_document_id = pending_id
        exc.pending_ident_hash = pending_ident_hash
        set_publication_failure(cursor, exc)

    try:
        validate_model(cursor, model)
    except exceptions.PublicationException as exc:
        exc_info = sys.exc_info()
        exc.publication_id = publication_id
        exc.pending_document_id = pending_id
        exc.pending_ident_hash = pending_ident_hash
        try:
            set_publication_failure(cursor, exc)
        except BaseException:
            import traceback
            print("Critical data error. Immediate attention is "
                  "required. On publication at '{}'."
                  .format(publication_id),
                  file=sys.stderr)
            # Print the critical exception.
            traceback.print_exc()
            # Raise the previous exception, so we know the original cause.
            raise exc_info[0], exc_info[1], exc_info[2]
    else:
        upsert_pending_licensors(cursor, pending_id)
        upsert_pending_roles(cursor, pending_id)
        notify_users(cursor, pending_id)
    return pending_ident_hash