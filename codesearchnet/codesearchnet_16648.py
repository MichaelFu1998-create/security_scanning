def get_finders():
    """
    Set the media fixtures finders on settings.py. 
    Example:
        MEDIA_FIXTURES_FILES_FINDERS = (
            'django_media_fixtures.finders.FileSystemFinder',
            'django_media_fixtures.finders.AppDirectoriesFinder',  # default
        )
    """
    if hasattr(settings, 'MEDIA_FIXTURES_FILES_FINDERS'):
        finders = settings.MEDIA_FIXTURES_FILES_FINDERS
    else:
        finders = (
            'django_media_fixtures.finders.AppDirectoriesFinder',
        )

    for finder_path in finders:
        yield get_finder(finder_path)