def bind_proxy(values, category=None, field=None, verbose_name=None, help_text='', static=True, readonly=False):
    """Binds PrefProxy objects to module variables used by apps as preferences.

    :param list|tuple values: Preference values.

    :param str|unicode category: Category name the preference belongs to.

    :param Field field: Django model field to represent this preference.

    :param str|unicode verbose_name: Field verbose name.

    :param str|unicode help_text: Field help text.

    :param bool static: Leave this preference static (do not store in DB).

    :param bool readonly: Make this field read only.

    :rtype: list

    """
    addrs = OrderedDict()

    depth = 3

    for local_name, locals_dict in traverse_local_prefs(depth):
        addrs[id(locals_dict[local_name])] = local_name

    proxies = []
    locals_dict = get_frame_locals(depth)

    for value in values:  # Try to preserve fields order.

        id_val = id(value)

        if id_val in addrs:
            local_name = addrs[id_val]
            local_val = locals_dict[local_name]

            if isinstance(local_val, PatchedLocal) and not isinstance(local_val, PrefProxy):

                proxy = PrefProxy(
                    local_name, value.val,
                    category=category,
                    field=field,
                    verbose_name=verbose_name,
                    help_text=help_text,
                    static=static,
                    readonly=readonly,
                )

                app_name = locals_dict['__name__'].split('.')[-2]  # x.y.settings -> y
                prefs = get_prefs()

                if app_name not in prefs:
                    prefs[app_name] = OrderedDict()

                prefs[app_name][local_name.lower()] = proxy

                # Replace original pref variable with a proxy.
                locals_dict[local_name] = proxy
                proxies.append(proxy)

    return proxies