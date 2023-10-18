def fromdict(cls, config, check_fields=True):
        """Create a Config object from config dict directly."""
        m = super(Config, cls).__new__(cls)
        m.path = '.'
        m.verbose = False
        m.config = m._merge_defaults(config)
        if check_fields:
            m._check_fields()
        return m