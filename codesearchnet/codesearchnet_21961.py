def setting(self, name_hyphen):
        """
        Retrieves the setting value whose name is indicated by name_hyphen.

        Values starting with $ are assumed to reference environment variables,
        and the value stored in environment variables is retrieved. It's an
        error if thes corresponding environment variable it not set.
        """
        if name_hyphen in self._instance_settings:
            value = self._instance_settings[name_hyphen][1]
        else:
            msg = "No setting named '%s'" % name_hyphen
            raise UserFeedback(msg)

        if hasattr(value, 'startswith') and value.startswith("$"):
            env_var = value.lstrip("$")
            if env_var in os.environ:
                return os.getenv(env_var)
            else:
                msg = "'%s' is not defined in your environment" % env_var
                raise UserFeedback(msg)

        elif hasattr(value, 'startswith') and value.startswith("\$"):
            return value.replace("\$", "$")

        else:
            return value