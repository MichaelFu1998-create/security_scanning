def get_pref_model_class(app, prefs, get_prefs_func):
    """Returns preferences model class dynamically crated for a given app or None on conflict."""

    module = '%s.%s' % (app, PREFS_MODULE_NAME)

    model_dict = {
            '_prefs_app': app,
            '_get_prefs': staticmethod(get_prefs_func),
            '__module__': module,
            'Meta': type('Meta', (models.options.Options,), {
                'verbose_name': _('Preference'),
                'verbose_name_plural': _('Preferences'),
                'app_label': app,
                'managed': False,
            })
    }

    for field_name, val_proxy in prefs.items():
        model_dict[field_name] = val_proxy.field

    model = type('Preferences', (models.Model,), model_dict)

    def fake_save_base(self, *args, **kwargs):

        updated_prefs = {
            f.name: getattr(self, f.name) for f in self._meta.fields if not isinstance(f, models.fields.AutoField)
        }

        app_prefs = self._get_prefs(self._prefs_app)

        for pref in app_prefs.keys():
            if pref in updated_prefs:
                app_prefs[pref].db_value = updated_prefs[pref]

        self.pk = self._prefs_app  # Make Django 1.7 happy.
        prefs_save.send(sender=self, app=self._prefs_app, updated_prefs=updated_prefs)

        return True

    model.save_base = fake_save_base

    return model