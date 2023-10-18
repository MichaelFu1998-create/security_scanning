def republish_binders(cursor, models):
    """Republish the Binders that share Documents in the publication context.
    This needs to be given all the models in the publication context."""
    documents = set([])
    binders = set([])
    history_mapping = {}  # <previous-ident-hash>: <current-ident-hash>
    if not isinstance(models, (list, tuple, set,)):
        raise TypeError("``models`` Must be a sequence of model objects."
                        "We were given: {}".format(models))
    for model in models:
        if isinstance(model, (cnxepub.Binder,)):
            binders.add(split_ident_hash(model.ident_hash)[0])
            for doc in cnxepub.flatten_to_documents(model):
                documents.add(split_ident_hash(doc.ident_hash))
        else:
            documents.add(split_ident_hash(model.ident_hash))

    to_be_republished = []
    # What binders are these documents a part of?
    for (uuid, version) in documents:
        ident_hash = join_ident_hash(uuid, version)
        previous_ident_hash = get_previous_publication(cursor, ident_hash)
        if previous_ident_hash is None:
            # Has no prior existence.
            continue
        else:
            history_mapping[previous_ident_hash] = ident_hash
        cursor.execute("""\
WITH RECURSIVE t(nodeid, parent_id, documentid, path) AS (
  SELECT tr.nodeid, tr.parent_id, tr.documentid, ARRAY[tr.nodeid]
  FROM trees tr
  WHERE tr.documentid = (
    SELECT module_ident FROM modules
    WHERE ident_hash(uuid, major_version, minor_version) = %s)
UNION ALL
  SELECT c.nodeid, c.parent_id, c.documentid, path || ARRAY[c.nodeid]
  FROM trees c JOIN t ON (c.nodeid = t.parent_id)
  WHERE not c.nodeid = ANY(t.path)
)
SELECT ident_hash(uuid, major_version, minor_version)
FROM t JOIN latest_modules m ON (t.documentid = m.module_ident)
WHERE t.parent_id IS NULL
""",
                       (previous_ident_hash,))
        to_be_republished.extend([split_ident_hash(x[0])
                                  for x in cursor.fetchall()])
    to_be_republished = set(to_be_republished)

    republished_ident_hashes = []
    # Republish the Collections set.
    for (uuid, version) in to_be_republished:
        if uuid in binders:
            # This binder is already in the publication context,
            # don't try to publish it again.
            continue
        ident_hash = join_ident_hash(uuid, version)
        bumped_version = bump_version(cursor, uuid, is_minor_bump=True)
        republished_ident_hash = republish_collection(cursor, ident_hash,
                                                      version=bumped_version)
        # Set the identifier history.
        history_mapping[ident_hash] = republished_ident_hash
        rebuild_collection_tree(cursor, ident_hash, history_mapping)
        republished_ident_hashes.append(republished_ident_hash)

    return republished_ident_hashes