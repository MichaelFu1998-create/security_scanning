def import_prefs():
    """Imports preferences modules from packages (apps) and project root."""
    
    # settings.py locals if autodiscover_siteprefs() is in urls.py
    settings_locals = get_frame_locals(3)

    if 'self' not in settings_locals:  # If not SiteprefsConfig.ready()
        # Try to import project-wide prefs.

        project_package = settings_locals['__package__']  # Expected project layout introduced in Django 1.4
        if not project_package:
            # Fallback to old layout.
            project_package = os.path.split(os.path.dirname(settings_locals['__file__']))[-1]

        import_module(project_package, PREFS_MODULE_NAME)

    import_project_modules(PREFS_MODULE_NAME)