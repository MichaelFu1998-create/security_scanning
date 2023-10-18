def pref_group(title, prefs, help_text='', static=True, readonly=False):
    """Marks preferences group.

    :param str|unicode title: Group title

    :param list|tuple prefs: Preferences to group.

    :param str|unicode help_text: Field help text.

    :param bool static: Leave this preference static (do not store in DB).

    :param bool readonly: Make this field read only.

    """
    bind_proxy(prefs, title, help_text=help_text, static=static, readonly=readonly)

    for proxy in prefs:  # For preferences already marked by pref().
        if isinstance(proxy, PrefProxy):
            proxy.category = title