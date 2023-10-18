def download_file(from_url, to_filename=None,
                  chunk_size=1024 * 8, retry_count=3):
    """Download URL to a file."""
    if not to_filename:
        to_filename = get_temporary_file()

    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=retry_count)
    session.mount(from_url, adapter)
    response = session.get(from_url, stream=True)
    with open(to_filename, 'wb') as fd:
        for chunk in response.iter_content(chunk_size):
            fd.write(chunk)
    return to_filename