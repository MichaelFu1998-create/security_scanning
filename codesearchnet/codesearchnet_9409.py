def setup_service(api_name, api_version, credentials=None):
  """Configures genomics API client.

  Args:
    api_name: Name of the Google API (for example: "genomics")
    api_version: Version of the API (for example: "v2alpha1")
    credentials: Credentials to be used for the gcloud API calls.

  Returns:
    A configured Google Genomics API client with appropriate credentials.
  """
  if not credentials:
    credentials = oauth2client.client.GoogleCredentials.get_application_default(
    )
  return apiclient.discovery.build(
      api_name, api_version, credentials=credentials)