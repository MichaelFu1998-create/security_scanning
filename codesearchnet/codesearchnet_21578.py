async def download_metadata_yaml(session, github_url):
    """Download the metadata.yaml file from a technote's GitHub repository.
    """
    metadata_yaml_url = _build_metadata_yaml_url(github_url)
    async with session.get(metadata_yaml_url) as response:
        response.raise_for_status()
        yaml_data = await response.text()
    return yaml.safe_load(yaml_data)