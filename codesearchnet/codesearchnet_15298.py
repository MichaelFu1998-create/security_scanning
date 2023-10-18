def get_connection(module_name: str, connection: Optional[str] = None) -> str:
    """Return the SQLAlchemy connection string if it is set.

    Order of operations:

    1. Return the connection if given as a parameter
    2. Check the environment for BIO2BEL_{module_name}_CONNECTION
    3. Look in the bio2bel config file for module-specific connection. Create if doesn't exist. Check the
       module-specific section for ``connection``
    4. Look in the bio2bel module folder for a config file. Don't create if doesn't exist. Check the default section
       for ``connection``
    5. Check the environment for BIO2BEL_CONNECTION
    6. Check the bio2bel config file for default
    7. Fall back to standard default cache connection

    :param module_name: The name of the module to get the configuration for
    :param connection: get the SQLAlchemy connection string
    :return: The SQLAlchemy connection string based on the configuration
    """
    # 1. Use given connection
    if connection is not None:
        return connection

    module_name = module_name.lower()
    module_config_cls = get_module_config_cls(module_name)
    module_config = module_config_cls.load()

    return module_config.connection or config.connection