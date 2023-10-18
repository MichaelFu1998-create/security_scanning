def get_user_agent_default(pkg_name='cloudaux'):
    """ 
    Get default User Agent String.

    Try to import pkg_name to get an accurate version number.
    
    return: string
    """
    version = '0.0.1'
    try:
        import pkg_resources
        version = pkg_resources.get_distribution(pkg_name).version
    except pkg_resources.DistributionNotFound:
        pass
    except ImportError:
        pass

    return 'cloudaux/%s' % (version)