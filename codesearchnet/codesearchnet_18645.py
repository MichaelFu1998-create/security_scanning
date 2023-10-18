def update_links_and_ffts(self):
        """FFT (856) Dealing with files."""
        for field in record_get_field_instances(self.record,
                                                tag='856',
                                                ind1='4'):
            subs = field_get_subfields(field)
            newsubs = []
            url = subs.get("u", [])

            if not url:
                record_delete_field(self.record, '856', ind1='4',
                                    field_position_global=field[4])
                continue
            url = url[0]
            if "inspirehep.net/record" in url and url.endswith("pdf"):
                # We have an FFT from INSPIRE
                newsubs.append(('a', url))
                description = subs.get("y", [])
                if description:
                    newsubs.append(('d', description[0]))
                if newsubs:
                    record_add_field(self.record, 'FFT', subfields=newsubs)
                    record_delete_field(self.record, '856', ind1='4',
                                        field_position_global=field[4])
            else:
                # Remove $w
                for idx, (key, value) in enumerate(field[0]):
                    if key == 'w':
                        del field[0][idx]