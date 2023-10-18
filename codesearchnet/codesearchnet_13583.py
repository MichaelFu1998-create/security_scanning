def add_setting(cls, name, type = unicode, default = None, factory = None,
                        cache = False, default_d = None, doc = None,
                        cmdline_help = None, validator = None, basic = False):
        """Add a new setting definition.

        :Parameters:
            - `name`: setting name
            - `type`: setting type object or type description
            - `default`: default value
            - `factory`: default value factory
            - `cache`: if `True` the `factory` will be called only once
              and its value stored as a constant default.
            - `default_d`: description of the default value
            - `doc`: setting documentation
            - `cmdline_help`: command line argument description. When not
              provided then the setting won't be available as a command-line
              option
            - `basic`: when `True` the option is considered a basic option -
              one of those which should usually stay configurable in
              an application.
            - `validator`: function validating command-line option value string
              and returning proper value for the settings objects. Defaults
              to `type`.
        :Types:
            - `name`: `unicode`
            - `type`: type or `unicode`
            - `factory`: a callable
            - `cache`: `bool`
            - `default_d`: `unicode`
            - `doc`: `unicode`
            - `cmdline_help`: `unicode`
            - `basic`: `bool`
            - `validator`: a callable
        """
        # pylint: disable-msg=W0622,R0913
        setting_def = _SettingDefinition(name, type, default, factory,
                                            cache, default_d, doc,
                                            cmdline_help, validator, basic)
        if name not in cls._defs:
            cls._defs[name] = setting_def
            return
        duplicate = cls._defs[name]
        if duplicate.type != setting_def.type:
            raise ValueError("Setting duplicate, with a different type")
        if duplicate.default != setting_def.default:
            raise ValueError("Setting duplicate, with a different default")
        if duplicate.factory != setting_def.factory:
            raise ValueError("Setting duplicate, with a different factory")