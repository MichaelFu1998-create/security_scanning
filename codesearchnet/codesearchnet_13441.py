def _decode_names(self):
        """Decode names (hopefully ASCII or UTF-8) into Unicode.
        """
        if self.subject_name is not None:
            subject_name = []
            for part in self.subject_name:
                new_part = []
                for name, value in part:
                    try:
                        name = name.decode("utf-8")
                        value = value.decode("utf-8")
                    except UnicodeError:
                        continue
                    new_part.append((name, value))
                subject_name.append(tuple(new_part))
            self.subject_name = tuple(subject_name)
        for key, old in self.alt_names.items():
            new = []
            for name in old:
                try:
                    name = name.decode("utf-8")
                except UnicodeError:
                    continue
                new.append(name)
            self.alt_names[key] = new