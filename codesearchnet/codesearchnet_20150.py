def pref(preference, field=None, verbose_name=None, help_text='', static=True, readonly=False):
    """Marks a preference.

    :param preference: Preference variable.

    :param Field field: Django model field to represent this preference.

    :param str|unicode verbose_name: Field verbose name.

    :param str|unicode help_text: Field help text.

    :param bool static: Leave this preference static (do not store in DB).

    :param bool readonly: Make this field read only.

    :rtype: PrefProxy|None
    """
    try:
        bound = bind_proxy(
            (preference,),
            field=field,
            verbose_name=verbose_name,
            help_text=help_text,
            static=static,
            readonly=readonly,
        )
        return bound[0]

    except IndexError:
        return