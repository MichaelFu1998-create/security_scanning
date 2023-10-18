def feature_uri(uri):
    """Decorating attaching a feature URI (for Service Discovery or Capability
    to a XMPPFeatureHandler class."""
    def decorator(class_):
        """Returns a decorated class"""
        if "_pyxmpp_feature_uris" not in class_.__dict__:
            class_._pyxmpp_feature_uris = set()
        class_._pyxmpp_feature_uris.add(uri)
        return class_
    return decorator