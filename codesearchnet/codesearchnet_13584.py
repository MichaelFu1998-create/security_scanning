def validate_string_list(value):
        """Validator for string lists to be used with `add_setting`."""
        try:
            if sys.version_info.major < 3:
                # pylint: disable-msg=W0404
                from locale import getpreferredencoding
                encoding = getpreferredencoding()
                value = value.decode(encoding)
            return [x.strip() for x in value.split(u",")]
        except (AttributeError, TypeError, UnicodeError):
            raise ValueError("Bad string list")