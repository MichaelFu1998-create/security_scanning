def _get_default_namespace(self) -> Optional[Namespace]:
        """Get the reference BEL namespace if it exists."""
        return self._get_query(Namespace).filter(Namespace.url == self._get_namespace_url()).one_or_none()