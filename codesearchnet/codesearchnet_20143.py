def register_admin_models(admin_site):
    """Registers dynamically created preferences models for Admin interface.

    :param admin.AdminSite admin_site: AdminSite object.

    """
    global __MODELS_REGISTRY

    prefs = get_prefs()

    for app_label, prefs_items in prefs.items():

        model_class = get_pref_model_class(app_label, prefs_items, get_app_prefs)

        if model_class is not None:
            __MODELS_REGISTRY[app_label] = model_class
            admin_site.register(model_class, get_pref_model_admin_class(prefs_items))