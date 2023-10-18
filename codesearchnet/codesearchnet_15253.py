def write_bel_annotation(self, file: TextIO) -> None:
        """Write as a BEL annotation file."""
        if not self.is_populated():
            self.populate()

        values = self._get_namespace_name_to_encoding(desc='writing names')

        write_annotation(
            keyword=self._get_namespace_keyword(),
            citation_name=self._get_namespace_name(),
            description='',
            values=values,
            file=file,
        )