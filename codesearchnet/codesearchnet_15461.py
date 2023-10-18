def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        for translation in orm['people.PersonTranslation'].objects.all():
            if translation.language in ['en', 'de']:
                translation.roman_first_name = translation.first_name
                translation.roman_last_name = translation.last_name
            else:
                translation.non_roman_first_name = translation.first_name
                translation.non_roman_last_name = translation.last_name
            translation.save()