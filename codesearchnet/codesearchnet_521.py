def download_file_from_google_drive(ID, destination):
    """Download file from Google Drive.

    See ``tl.files.load_celebA_dataset`` for example.

    Parameters
    --------------
    ID : str
        The driver ID.
    destination : str
        The destination for save file.

    """

    def save_response_content(response, destination, chunk_size=32 * 1024):
        total_size = int(response.headers.get('content-length', 0))
        with open(destination, "wb") as f:
            for chunk in tqdm(response.iter_content(chunk_size), total=total_size, unit='B', unit_scale=True,
                              desc=destination):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params={'id': ID}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': ID, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    save_response_content(response, destination)