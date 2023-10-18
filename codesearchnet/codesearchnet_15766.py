def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        LEN_TYPE = {
            7: 'GMI',
            4: 'POW',
            2: 'WOJ',
        }
        for ja in orm.JednostkaAdministracyjna.objects.all():
            ja.typ = LEN_TYPE[len(ja.id)]
            ja.save()