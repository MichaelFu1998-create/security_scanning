def on_pref_update(*args, **kwargs):
    """Triggered on dynamic preferences model save.
     Issues DB save and reread.

    """
    Preference.update_prefs(*args, **kwargs)
    Preference.read_prefs(get_prefs())