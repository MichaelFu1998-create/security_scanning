def _get_storage_service(credentials):
  """Get a storage client using the provided credentials or defaults."""
  if credentials is None:
    credentials = oauth2client.client.GoogleCredentials.get_application_default(
    )
  return discovery.build('storage', 'v1', credentials=credentials)