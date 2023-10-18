def forwards(self, orm):
        "Write your forwards methods here."
        for translation in orm['people.PersonTranslation'].objects.all():
            translation.person.roman_first_name = translation.roman_first_name
            translation.person.roman_last_name = translation.roman_last_name
            translation.person.non_roman_first_name = translation.non_roman_first_name
            translation.person.non_roman_last_name = translation.non_roman_last_name
            translation.person.save()