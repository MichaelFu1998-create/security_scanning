def create_meta_data(cls, options, args, parser):
        """
        Override in subclass if required.
        """
        meta_data = []
        meta_data.append(('spiff_version', cls.get_version()))
        if options.target_engine:
            meta_data.append(('target_engine', options.target_engine))
        if options.target_engine:
            meta_data.append(
                ('target_engine_version', options.target_engine_version))
        return meta_data