def get_storage(request):
    """ Gets a Credentials storage object provided by the Django OAuth2 Helper
    object.

    Args:
        request: Reference to the current request object.

    Returns:
       An :class:`oauth2.client.Storage` object.
    """
    storage_model = oauth2_settings.storage_model
    user_property = oauth2_settings.storage_model_user_property
    credentials_property = oauth2_settings.storage_model_credentials_property

    if storage_model:
        module_name, class_name = storage_model.rsplit('.', 1)
        module = importlib.import_module(module_name)
        storage_model_class = getattr(module, class_name)
        return storage.DjangoORMStorage(storage_model_class,
                                        user_property,
                                        request.user,
                                        credentials_property)
    else:
        # use session
        return dictionary_storage.DictionaryStorage(
            request.session, key=_CREDENTIALS_KEY)