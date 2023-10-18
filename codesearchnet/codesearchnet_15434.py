def rebuild_collection_tree(cursor, ident_hash, history_map):
    """Create a new tree for the collection based on the old tree but with
    new document ids
    """
    collection_tree_sql = """\
WITH RECURSIVE t(nodeid, parent_id, documentid, title, childorder, latest,
                 ident_hash, path) AS (
  SELECT
    tr.nodeid, tr.parent_id, tr.documentid,
    tr.title, tr.childorder, tr.latest,
    (SELECT ident_hash(uuid, major_version, minor_version)
     FROM modules
     WHERE module_ident = tr.documentid) AS ident_hash,
    ARRAY[tr.nodeid]
  FROM trees AS tr
  WHERE tr.documentid = (
    SELECT module_ident
    FROM modules
    WHERE ident_hash(uuid, major_version, minor_version) = %s)
    AND tr.is_collated = FALSE
UNION ALL
  SELECT
    c.nodeid, c.parent_id, c.documentid, c.title, c.childorder, c.latest,
    (SELECT ident_hash(uuid, major_version, minor_version)
     FROM modules
     WHERE module_ident = c.documentid) AS ident_hash,
    path || ARRAY[c.nodeid]
  FROM trees AS c JOIN t ON (c.parent_id = t.nodeid)
  WHERE not c.nodeid = ANY(t.path) AND c.is_collated = FALSE
)
SELECT row_to_json(row) FROM (SELECT * FROM t) AS row"""

    tree_insert_sql = """\
INSERT INTO trees
  (nodeid, parent_id,
   documentid,
   title, childorder, latest)
VALUES
  (DEFAULT, %(parent_id)s,
   (SELECT module_ident
    FROM modules
    WHERE ident_hash(uuid, major_version, minor_version) = \
          %(ident_hash)s),
   %(title)s, %(childorder)s, %(latest)s)
RETURNING nodeid"""

    def get_tree():
        cursor.execute(collection_tree_sql, (ident_hash,))
        for row in cursor.fetchall():
            yield row[0]

    def insert(fields):
        cursor.execute(tree_insert_sql, fields)
        results = cursor.fetchone()[0]
        return results

    tree = {}  # {<current-nodeid>: {<row-data>...}, ...}
    children = {}  # {<nodeid>: [<child-nodeid>, ...], <child-nodeid>: [...]}
    for node in get_tree():
        tree[node['nodeid']] = node
        children.setdefault(node['parent_id'], [])
        children[node['parent_id']].append(node['nodeid'])

    def build_tree(nodeid, parent_id):
        data = tree[nodeid]
        data['parent_id'] = parent_id
        if history_map.get(data['ident_hash']) is not None \
           and (data['latest'] or parent_id is None):
            data['ident_hash'] = history_map[data['ident_hash']]
        new_nodeid = insert(data)
        for child_nodeid in children.get(nodeid, []):
            build_tree(child_nodeid, new_nodeid)

    root_node = children[None][0]
    build_tree(root_node, None)