def _import_mapping(mapping, original=None):
    """Import any string-keys in a type mapping."""
    #log = get_logger()
    #log.debug("Importing canning map")
    for key, value in list(mapping.items()):
        if isinstance(key, string_types):
            try:
                cls = import_item(key)
            except Exception:
                if original and key not in original:
                    # only message on user-added classes
                    # log.error("canning class not importable: %r", key, exc_info=True)
                    print("ERROR: canning class not importable: %r", key, exc_info=True)
                mapping.pop(key)
            else:
                mapping[cls] = mapping.pop(key)