def _get_old_entry_identifiers(namespace: Namespace) -> Set[NamespaceEntry]:
        """Convert a PyBEL generalized namespace entries to a set.

        Default to using the identifier, but can be overridden to use the name instead.

        >>> {term.identifier for term in namespace.entries}
        """
        return {term.identifier for term in namespace.entries}