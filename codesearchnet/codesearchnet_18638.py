def update_journals(self):
        """773 journal translations."""
        for field in record_get_field_instances(self.record, '773'):
            subs = field_get_subfield_instances(field)
            new_subs = []
            volume_letter = ""
            journal_name = ""
            for idx, (key, value) in enumerate(subs):
                if key == 'p':
                    journal_name = self.get_config_item(value, "journals", allow_substring=False)
                    # Make sure journal names have the form (dot)(space) (I know it's horrible)
                    journal_name = journal_name.replace('. ', '.').replace('.', '. ').replace('. ,', '.,').strip()
                elif key == 'v':
                    volume_letter = value
                else:
                    new_subs.append((key, value))

            if not journal_name == "PoS":
                # Special handling of journal name and volumes, except PoS
                letter = return_letters_from_string(volume_letter)
                if letter:
                    journal_name = "{0} {1}".format(journal_name, letter)
                    volume_letter = volume_letter.strip(letter)

            if journal_name:
                new_subs.append(("p", journal_name))
            if volume_letter:
                new_subs.append(("v", volume_letter))
            record_delete_field(self.record, tag="773",
                                field_position_global=field[4])
            record_add_field(self.record, "773", subfields=new_subs)