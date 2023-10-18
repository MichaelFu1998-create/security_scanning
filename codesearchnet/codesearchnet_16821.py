def location():
    """Load default location."""
    d = current_app.config['DATADIR']
    with db.session.begin_nested():
        Location.query.delete()
        loc = Location(name='local', uri=d, default=True)
        db.session.add(loc)
    db.session.commit()