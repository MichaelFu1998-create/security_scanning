def import_gtfs(gtfs_sources, output, preserve_connection=False,
                print_progress=True, location_name=None, **kwargs):
    """Import a GTFS database

    gtfs_sources: str, dict, list
        Paths to the gtfs zip file or to the directory containing the GTFS data.
        Alternatively, a dict can be provide that maps gtfs filenames
        (like 'stops.txt' and 'agencies.txt') to their string presentations.

    output: str or sqlite3.Connection
        path to the new database to be created, or an existing
        sqlite3 connection
    preserve_connection: bool, optional
        Whether to close the connection in the end, or not.
    print_progress: bool, optional
        Whether to print progress output
    location_name: str, optional
        set the location of this database
    """
    if isinstance(output, sqlite3.Connection):
        conn = output
    else:
        # if os.path.isfile(output):
        #  raise RuntimeError('File already exists')
        conn = sqlite3.connect(output)
    if not isinstance(gtfs_sources, list):
        gtfs_sources = [gtfs_sources]
    cur = conn.cursor()
    time_import_start = time.time()

    # These are a bit unsafe, but make importing much faster,
    # especially on scratch.
    cur.execute('PRAGMA page_size = 4096;')
    cur.execute('PRAGMA mmap_size = 1073741824;')
    cur.execute('PRAGMA cache_size = -2000000;')
    cur.execute('PRAGMA temp_store=2;')
    # Changes of isolation level are python3.6 workarounds -
    # eventually will probably be fixed and this can be removed.
    conn.isolation_level = None  # change to autocommit mode (former default)
    cur.execute('PRAGMA journal_mode = OFF;')
    #cur.execute('PRAGMA journal_mode = WAL;')
    cur.execute('PRAGMA synchronous = OFF;')
    conn.isolation_level = ''    # change back to python default.
    # end python3.6 workaround

    # Do the actual importing.
    loaders = [L(gtfssource=gtfs_sources, print_progress=print_progress, **kwargs) for L in Loaders]

    for loader in loaders:
        loader.assert_exists_if_required()

    # Do initial import.  This consists of making tables, raw insert
    # of the CSVs, and then indexing.

    for loader in loaders:
        loader.import_(conn)

    # Do any operations that require all tables present.
    for Loader in loaders:
        Loader.post_import_round2(conn)

    # Make any views
    for Loader in loaders:
        Loader.make_views(conn)

    # Make any views
    for F in postprocessors:
        F(conn)

    # Set up same basic metadata.
    from gtfspy import gtfs as mod_gtfs
    G = mod_gtfs.GTFS(output)
    G.meta['gen_time_ut'] = time.time()
    G.meta['gen_time'] = time.ctime()
    G.meta['import_seconds'] = time.time() - time_import_start
    G.meta['download_date'] = ''
    G.meta['location_name'] = ''
    G.meta['n_gtfs_sources'] = len(gtfs_sources)

    # Extract things from GTFS
    download_date_strs = []
    for i, source in enumerate(gtfs_sources):
        if len(gtfs_sources) == 1:
            prefix = ""
        else:
            prefix = "feed_" + str(i) + "_"
        if isinstance(source, string_types):
            G.meta[prefix + 'original_gtfs'] = decode_six(source) if source else None
            # Extract GTFS date.  Last date pattern in filename.
            filename_date_list = re.findall(r'\d{4}-\d{2}-\d{2}', source)
            if filename_date_list:
                date_str = filename_date_list[-1]
                G.meta[prefix + 'download_date'] = date_str
                download_date_strs.append(date_str)
            if location_name:
                G.meta['location_name'] = location_name
            else:
                location_name_list = re.findall(r'/([^/]+)/\d{4}-\d{2}-\d{2}', source)
                if location_name_list:
                    G.meta[prefix + 'location_name'] = location_name_list[-1]
                else:
                    try:
                        G.meta[prefix + 'location_name'] = source.split("/")[-4]
                    except:
                        G.meta[prefix + 'location_name'] = source

    if G.meta['download_date'] == "":
        unique_download_dates = list(set(download_date_strs))
        if len(unique_download_dates) == 1:
            G.meta['download_date'] = unique_download_dates[0]

    G.meta['timezone'] = cur.execute('SELECT timezone FROM agencies LIMIT 1').fetchone()[0]
    stats.update_stats(G)
    del G

    if print_progress:
        print("Vacuuming...")
    # Next 3 lines are python 3.6 work-arounds again.
    conn.isolation_level = None  # former default of autocommit mode
    cur.execute('VACUUM;')
    conn.isolation_level = ''    # back to python default
    # end python3.6 workaround
    if print_progress:
        print("Analyzing...")
    cur.execute('ANALYZE')
    if not (preserve_connection is True):
        conn.close()