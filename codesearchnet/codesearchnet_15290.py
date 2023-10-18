def create_all(engine, checkfirst=True):
    """Create the tables for Bio2BEL."""
    Base.metadata.create_all(bind=engine, checkfirst=checkfirst)