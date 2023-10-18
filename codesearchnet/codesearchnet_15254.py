def write_bel_namespace_mappings(self, file: TextIO, **kwargs) -> None:
        """Write a BEL namespace mapping file."""
        json.dump(self._get_namespace_identifier_to_name(**kwargs), file, indent=2, sort_keys=True)