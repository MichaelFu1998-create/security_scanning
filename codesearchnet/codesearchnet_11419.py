def set_mappings(cls, index_name, doc_type, mappings):
        """ set new mapped-items structure into cache """
        cache.set(cls.get_cache_item_name(index_name, doc_type), mappings)