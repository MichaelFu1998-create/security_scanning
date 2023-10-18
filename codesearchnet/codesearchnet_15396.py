def publish_pending(cursor, publication_id):
    """Given a publication id as ``publication_id``,
    write the documents to the *Connexions Archive*.
    """
    cursor.execute("""\
WITH state_update AS (
  UPDATE publications SET state = 'Publishing' WHERE id = %s
)
SELECT publisher, publication_message
FROM publications
WHERE id = %s""",
                   (publication_id, publication_id,))
    publisher, message = cursor.fetchone()
    cursor.connection.commit()

    all_models = []

    from .publish import publish_model
    # Commit documents one at a time...
    type_ = cnxepub.Document.__name__
    cursor.execute("""\
SELECT id, uuid, major_version, minor_version, metadata, content
FROM pending_documents
WHERE type = %s AND publication_id = %s""", (type_, publication_id,))
    for row in cursor.fetchall():
        # FIXME Oof, this is hideous!
        id, major_version, minor_version = row[1:4]
        id = str(id)
        version = '.'.join([str(x)
                            for x in (major_version, minor_version,)
                            if x is not None])
        metadata, content = row[-2:]
        content = content[:]
        metadata['version'] = version

        document = cnxepub.Document(id, content, metadata)
        for ref in document.references:
            if ref.uri.startswith('/resources/'):
                hash = ref.uri[len('/resources/'):]
                cursor.execute("""\
SELECT data, media_type
FROM pending_resources
WHERE hash = %s""", (hash,))
                data, media_type = cursor.fetchone()
                document.resources.append(cnxepub.Resource(
                    hash, io.BytesIO(data[:]), media_type, filename=hash))

        _ident_hash = publish_model(cursor, document, publisher, message)  # noqa
        all_models.append(document)

    # And now the binders, one at a time...
    type_ = cnxepub.Binder.__name__
    cursor.execute("""\
SELECT id, uuid, major_version, minor_version, metadata, content
FROM pending_documents
WHERE type = %s AND publication_id = %s""", (type_, publication_id,))
    for row in cursor.fetchall():
        id, major_version, minor_version, metadata = row[1:5]
        tree = metadata['_tree']
        binder = _reassemble_binder(str(id), tree, metadata)
        # Add the resources
        cursor.execute("""\
SELECT hash, data, media_type, filename
FROM pending_resources r
JOIN pending_resource_associations a ON a.resource_id = r.id
JOIN pending_documents d ON a.document_id = d.id
WHERE ident_hash(uuid, major_version, minor_version) = %s""",
                       (binder.ident_hash,))
        binder.resources = [
            cnxepub.Resource(r_hash,
                             io.BytesIO(r_data[:]),
                             r_media_type,
                             filename=r_filename)
            for (r_hash, r_data, r_media_type, r_filename)
            in cursor.fetchall()]
        _ident_hash = publish_model(cursor, binder, publisher, message)  # noqa
        all_models.append(binder)

    # Republish binders containing shared documents.
    from .publish import republish_binders
    _republished_ident_hashes = republish_binders(cursor, all_models)  # noqa

    # Lastly, update the publication status.
    cursor.execute("""\
UPDATE publications
SET state = 'Done/Success'
WHERE id = %s
RETURNING state""", (publication_id,))
    state = cursor.fetchone()[0]
    return state