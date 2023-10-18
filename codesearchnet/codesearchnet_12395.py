def prepare_docset(
    source, dest, name, index_page, enable_js, online_redirect_url
):
    """
    Create boilerplate files & directories and copy vanilla docs inside.

    Return a tuple of path to resources and connection to sqlite db.
    """
    resources = os.path.join(dest, "Contents", "Resources")
    docs = os.path.join(resources, "Documents")
    os.makedirs(resources)

    db_conn = sqlite3.connect(os.path.join(resources, "docSet.dsidx"))
    db_conn.row_factory = sqlite3.Row
    db_conn.execute(
        "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, "
        "type TEXT, path TEXT)"
    )
    db_conn.commit()

    plist_path = os.path.join(dest, "Contents", "Info.plist")
    plist_cfg = {
        "CFBundleIdentifier": name,
        "CFBundleName": name,
        "DocSetPlatformFamily": name.lower(),
        "DashDocSetFamily": "python",
        "isDashDocset": True,
        "isJavaScriptEnabled": enable_js,
    }
    if index_page is not None:
        plist_cfg["dashIndexFilePath"] = index_page
    if online_redirect_url is not None:
        plist_cfg["DashDocSetFallbackURL"] = online_redirect_url

    write_plist(plist_cfg, plist_path)

    shutil.copytree(source, docs)

    return DocSet(path=dest, docs=docs, plist=plist_path, db_conn=db_conn)