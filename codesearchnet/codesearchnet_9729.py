def main_make_views(gtfs_fname):
    """Re-create all views.
    """
    print("creating views")
    conn = GTFS(fname_or_conn=gtfs_fname).conn
    for L in Loaders:
        L(None).make_views(conn)
    conn.commit()