def autodiscover_siteprefs(admin_site=None):
    """Automatically discovers and registers all preferences available in all apps.

    :param admin.AdminSite admin_site: Custom AdminSite object.

    """
    if admin_site is None:
        admin_site = admin.site

    # Do not discover anything if called from manage.py (e.g. executing commands from cli).
    if 'manage' not in sys.argv[0] or (len(sys.argv) > 1 and sys.argv[1] in MANAGE_SAFE_COMMANDS):
        import_prefs()
        Preference.read_prefs(get_prefs())
        register_admin_models(admin_site)