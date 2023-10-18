def get(self, section, option, **kwargs):  # type: ignore
        # type: (str, str, Any) -> Any
        """
        Overrides :py:meth:`configparser.ConfigParser.get`.

        In addition to ``section`` and ``option``, this call takes an optional
        ``default`` value. This behaviour works in *addition* to the
        :py:class:`configparser.ConfigParser` default mechanism. Note that
        a default value from ``ConfigParser`` takes precedence.

        The reason this additional functionality is added, is because the
        defaults of :py:class:`configparser.ConfigParser` are not dependent
        on sections. If you specify a default for the option ``test``, then
        this value will be returned for both ``section1.test`` and for
        ``section2.test``. Using the default on the ``get`` call gives you more
        fine-grained control over this.

        Also note, that if a default value was used, it will be logged with
        level ``logging.DEBUG``.

        :param section: The config file section.
        :param option: The option name.
        :param kwargs: These keyword args are passed through to
                       :py:meth:`configparser.ConfigParser.get`.
        """
        if "default" in kwargs:
            default = kwargs.pop("default")
            new_kwargs = {'fallback': default}
            new_kwargs.update(kwargs)
            new_call = build_call_str('.get', (section, option), new_kwargs)
            warn('Using the "default" argument to Config.get() will no '
                 'longer work in config_resolver 5.0! Version 5 will return '
                 'standard Python ConfigParser instances which use "fallback" '
                 'instead of "default". Replace your code with "%s"' % new_call,
                 DeprecationWarning,
                 stacklevel=2)
            have_default = True
        else:
            have_default = False

        try:
            value = super(Config, self).get(section, option, **kwargs)
            return value
        except (NoSectionError, NoOptionError) as exc:
            if have_default:
                self._log.debug("%s: Returning default value %r", exc, default)
                return default
            else:
                raise