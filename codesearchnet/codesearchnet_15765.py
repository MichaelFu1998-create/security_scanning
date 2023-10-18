def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        print("Updating: JednostkaAdministracyjna")
        ja_akt_stan=orm.JednostkaAdministracyjna.objects.all().aggregate(Max('stan_na'))['stan_na__max']
        orm.JednostkaAdministracyjna.objects.filter(stan_na__exact=ja_akt_stan).update(aktywny=True)
        orm.JednostkaAdministracyjna.objects.exclude(stan_na__exact=ja_akt_stan).update(aktywny=False)

        print("Updating: Miejscowosc")
        m_akt_stan=orm.Miejscowosc.objects.all().aggregate(Max('stan_na'))['stan_na__max']
        orm.Miejscowosc.objects.filter(stan_na__exact=m_akt_stan).update(aktywny=True)
        orm.Miejscowosc.objects.exclude(stan_na__exact=m_akt_stan).update(aktywny=False)

        print("Updating: RodzajMiejsowosci")
        rm_akt_stan=orm.RodzajMiejsowosci.objects.all().aggregate(Max('stan_na'))['stan_na__max']
        orm.RodzajMiejsowosci.objects.filter(stan_na__exact=rm_akt_stan).update(aktywny=True)
        orm.RodzajMiejsowosci.objects.exclude(stan_na__exact=rm_akt_stan).update(aktywny=False)

        print("Updating: Ulica")
        u_akt_stan=orm.Ulica.objects.all().aggregate(Max('stan_na'))['stan_na__max']
        orm.Ulica.objects.filter(stan_na__exact=u_akt_stan).update(aktywny=True)
        orm.Ulica.objects.exclude(stan_na__exact=u_akt_stan).update(aktywny=False)