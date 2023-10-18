def to_cldf(self, dest, mdname='cldf-metadata.json'):
        """
        Write the data from the db to a CLDF dataset according to the metadata in `self.dataset`.

        :param dest:
        :param mdname:
        :return: path of the metadata file
        """
        dest = Path(dest)
        if not dest.exists():
            dest.mkdir()

        data = self.read()

        if data[self.source_table_name]:
            sources = Sources()
            for src in data[self.source_table_name]:
                sources.add(Source(
                    src['genre'],
                    src['id'],
                    **{k: v for k, v in src.items() if k not in ['id', 'genre']}))
            sources.write(dest / self.dataset.properties.get('dc:source', 'sources.bib'))

        for table_type, items in data.items():
            try:
                table = self.dataset[table_type]
                table.common_props['dc:extent'] = table.write(
                    [self.retranslate(table, item) for item in items],
                    base=dest)
            except KeyError:
                assert table_type == self.source_table_name, table_type
        return self.dataset.write_metadata(dest / mdname)