def to_dict(self, include_meta=False):
        """
            Returns the result as a dictionary, provide the include_meta flag to als show information like index and doctype.
        """
        result = super(JackalDoc, self).to_dict(include_meta=include_meta)
        if include_meta:
            source = result.pop('_source')
            return {**result, **source}
        else:
            return result