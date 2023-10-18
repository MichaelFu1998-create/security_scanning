def get_config_item(cls, key, kb_name, allow_substring=True):
        """Return the opposite mapping by searching the imported KB."""
        config_dict = cls.kbs.get(kb_name, None)
        if config_dict:
            if key in config_dict:
                return config_dict[key]
            elif allow_substring:
                res = [v for k, v in config_dict.items() if key in k]
                if res:
                    return res[0]
        return key