def get_mongoadmins(self):
        """ Returns a list of all mongoadmin implementations for the site """
        apps = []
        for app_name in settings.INSTALLED_APPS:
            mongoadmin = "{0}.mongoadmin".format(app_name)
            try:
                module = import_module(mongoadmin)
            except ImportError as e:
                if str(e).startswith("No module named"):
                    continue
                raise e

            app_store = AppStore(module)
            apps.append(dict(
                app_name=app_name,
                obj=app_store
            ))
        return apps