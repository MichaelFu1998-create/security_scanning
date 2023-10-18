def register_prefs(*args, **kwargs):
    """Registers preferences that should be handled by siteprefs.

    Expects preferences as *args.

    Use keyword arguments to batch apply params supported by
    ``PrefProxy`` to all preferences not constructed by ``pref`` and ``pref_group``.

    Batch kwargs:

        :param str|unicode help_text: Field help text.

        :param bool static: Leave this preference static (do not store in DB).

        :param bool readonly: Make this field read only.

    :param bool swap_settings_module: Whether to automatically replace settings module
        with a special ``ProxyModule`` object to access dynamic values of settings
        transparently (so not to bother with calling ``.value`` of ``PrefProxy`` object).

    """
    swap_settings_module = bool(kwargs.get('swap_settings_module', True))

    if __PATCHED_LOCALS_SENTINEL not in get_frame_locals(2):
        raise SitePrefsException('Please call `patch_locals()` right before the `register_prefs()`.')

    bind_proxy(args, **kwargs)

    unpatch_locals()

    swap_settings_module and proxy_settings_module()