def load_config(from_key, to_key):
        """Load configuration from config.

        Meant to run only once per system process as
        class variable in subclasses."""
        from .mappings import mappings
        kbs = {}
        for key, values in mappings['config'].iteritems():
            parse_dict = {}
            for mapping in values:
                # {'inspire': 'Norwegian', 'cds': 'nno'}
                # -> {"Norwegian": "nno"}
                parse_dict[mapping[from_key]] = mapping[to_key]
            kbs[key] = parse_dict
        return kbs