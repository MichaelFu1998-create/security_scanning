def get_mappings(cls, index_name, doc_type):
        """ fetch mapped-items structure from cache """
        return cache.get(cls.get_cache_item_name(index_name, doc_type), {})