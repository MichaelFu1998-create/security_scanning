def register_range_type(pgrange, pyrange, conn):
    """
    Register a new range type as a PostgreSQL range.

        >>> register_range_type("int4range", intrange, conn)

    The above will make sure intrange is regarded as an int4range for queries
    and that int4ranges will be cast into intrange when fetching rows.

    pgrange should be the full name including schema for the custom range type.

    Note that adaption is global, meaning if a range type is passed to a regular
    psycopg2 connection it will adapt it to its proper range type. Parsing of
    rows from the database however is not global and just set on a per connection
    basis.
    """

    register_adapter(pyrange, partial(adapt_range, pgrange))
    register_range_caster(
        pgrange, pyrange, *query_range_oids(pgrange, conn), scope=conn)