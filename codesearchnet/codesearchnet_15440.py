def includeme(config):
    """Configures the caching manager"""
    global cache_manager
    settings = config.registry.settings
    cache_manager = CacheManager(**parse_cache_config_options(settings))