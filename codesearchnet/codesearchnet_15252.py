def write_bel_namespace(self, file: TextIO, use_names: bool = False) -> None:
        """Write as a BEL namespace file."""
        if not self.is_populated():
            self.populate()

        if use_names and not self.has_names:
            raise ValueError

        values = (
            self._get_namespace_name_to_encoding(desc='writing names')
            if use_names else
            self._get_namespace_identifier_to_encoding(desc='writing identifiers')
        )

        write_namespace(
            namespace_name=self._get_namespace_name(),
            namespace_keyword=self._get_namespace_keyword(),
            namespace_query_url=self.identifiers_url,
            values=values,
            file=file,
        )