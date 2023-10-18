def republish_collection(cursor, ident_hash, version):
    """Republish the collection identified as ``ident_hash`` with
    the given ``version``.
    """
    if not isinstance(version, (list, tuple,)):
        split_version = version.split('.')
        if len(split_version) == 1:
            split_version.append(None)
        version = tuple(split_version)
    major_version, minor_version = version

    cursor.execute("""\
WITH previous AS (
  SELECT module_ident
  FROM modules
  WHERE ident_hash(uuid, major_version, minor_version) = %s),
inserted AS (
  INSERT INTO modules
    (uuid, major_version, minor_version, revised,
     portal_type, moduleid,
     name, created, language,
     submitter, submitlog,
     abstractid, licenseid, parent, parentauthors,
     authors, maintainers, licensors,
     google_analytics, buylink,
     stateid, doctype)
  SELECT
    uuid, %s, %s, CURRENT_TIMESTAMP,
    portal_type, moduleid,
    name, created, language,
    submitter, submitlog,
    abstractid, licenseid, parent, parentauthors,
    authors, maintainers, licensors,
    google_analytics, buylink,
    stateid, doctype
  FROM modules AS m JOIN previous AS p ON (m.module_ident = p.module_ident)
  RETURNING
    ident_hash(uuid, major_version, minor_version) AS ident_hash,
    module_ident),
keywords AS (
  INSERT INTO modulekeywords (module_ident, keywordid)
  SELECT i.module_ident, keywordid
  FROM modulekeywords AS mk, inserted AS i, previous AS p
  WHERE mk.module_ident = p.module_ident),
tags AS (
  INSERT INTO moduletags (module_ident, tagid)
  SELECT i.module_ident, tagid
  FROM moduletags AS mt, inserted AS i, previous AS p
  WHERE mt.module_ident = p.module_ident)
SELECT ident_hash FROM inserted""",
                   (ident_hash, major_version, minor_version,))
    repub_ident_hash = cursor.fetchone()[0]
    return repub_ident_hash