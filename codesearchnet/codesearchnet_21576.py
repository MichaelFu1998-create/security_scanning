async def process_sphinx_technote(session, github_api_token, ltd_product_data,
                                  mongo_collection=None):
    """Extract, transform, and load Sphinx-based technote metadata.

    Parameters
    ----------
    session : `aiohttp.ClientSession`
        Your application's aiohttp client session.
        See http://aiohttp.readthedocs.io/en/stable/client.html.
    github_api_token : `str`
        A GitHub personal API token. See the `GitHub personal access token
        guide`_.
    ltd_product_data : `dict`
        Contents of ``metadata.yaml``, obtained via `download_metadata_yaml`.
        Data for this technote from the LTD Keeper API
        (``GET /products/<slug>``). Usually obtained via
        `lsstprojectmeta.ltd.get_ltd_product`.
    mongo_collection : `motor.motor_asyncio.AsyncIOMotorCollection`, optional
        MongoDB collection. This should be the common MongoDB collection for
        LSST projectmeta JSON-LD records. If provided, ths JSON-LD is upserted
        into the MongoDB collection.

    Returns
    -------
    metadata : `dict`
        JSON-LD-formatted dictionary.

    Raises
    ------
    NotSphinxTechnoteError
        Raised when the LTD product cannot be interpreted as a Sphinx-based
        technote project because it's missing a metadata.yaml file in its
        GitHub repository. This implies that the LTD product *could* be of a
        different format.

    .. `GitHub personal access token guide`: https://ls.st/41d
    """
    logger = logging.getLogger(__name__)

    github_url = ltd_product_data['doc_repo']
    github_url = normalize_repo_root_url(github_url)
    repo_slug = parse_repo_slug_from_url(github_url)

    try:
        metadata_yaml = await download_metadata_yaml(session, github_url)
    except aiohttp.ClientResponseError as err:
        # metadata.yaml not found; probably not a Sphinx technote
        logger.debug('Tried to download %s\'s metadata.yaml, got status %d',
                     ltd_product_data['slug'], err.code)
        raise NotSphinxTechnoteError()

    # Extract data from the GitHub API
    github_query = GitHubQuery.load('technote_repo')
    github_variables = {
        "orgName": repo_slug.owner,
        "repoName": repo_slug.repo
    }
    github_data = await github_request(session, github_api_token,
                                       query=github_query,
                                       variables=github_variables)

    try:
        jsonld = reduce_technote_metadata(
            github_url, metadata_yaml, github_data, ltd_product_data)
    except Exception as exception:
        message = "Issue building JSON-LD for technote %s"
        logger.exception(message, github_url, exception)
        raise

    if mongo_collection is not None:
        await _upload_to_mongodb(mongo_collection, jsonld)

    logger.info('Ingested technote %s into MongoDB', github_url)

    return jsonld