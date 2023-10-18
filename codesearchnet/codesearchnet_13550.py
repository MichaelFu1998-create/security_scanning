def _make_ns_declarations(declarations, declared_prefixes):
        """Build namespace declarations and remove obsoleted mappings
        from `declared_prefixes`.

        :Parameters:
            - `declarations`: namespace to prefix mapping of the new
              declarations
            - `declared_prefixes`: namespace to prefix mapping of already
              declared prefixes.
        :Types:
            - `declarations`: `unicode` to `unicode` dictionary
            - `declared_prefixes`: `unicode` to `unicode` dictionary

        :Return: string of namespace declarations to be used in a start tag
        :Returntype: `unicode`
        """
        result = []
        for namespace, prefix in declarations.items():
            if prefix:
                result.append(u' xmlns:{0}={1}'.format(prefix, quoteattr(
                                                                namespace)))
            else:
                result.append(u' xmlns={1}'.format(prefix, quoteattr(
                                                                namespace)))
            for d_namespace, d_prefix in declared_prefixes.items():
                if (not prefix and not d_prefix) or d_prefix == prefix:
                    if namespace != d_namespace:
                        del declared_prefixes[d_namespace]
        return u" ".join(result)