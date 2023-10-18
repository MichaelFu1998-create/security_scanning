def from_directory_as_inmemory_db(cls, gtfs_directory):
        """
        Instantiate a GTFS object by computing

        Parameters
        ----------
        gtfs_directory: str
            path to the directory for importing the database
        """
        # this import is here to avoid circular imports (which turned out to be a problem)
        from gtfspy.import_gtfs import import_gtfs
        conn = sqlite3.connect(":memory:")
        import_gtfs(gtfs_directory,
                    conn,
                    preserve_connection=True,
                    print_progress=False)
        return cls(conn)