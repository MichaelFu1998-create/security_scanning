async def process_ltd_doc(session, github_api_token, ltd_product_url,
                          mongo_collection=None):
    """Ingest any kind of LSST document hosted on LSST the Docs from its
    source.

    Parameters
    ----------
    session : `aiohttp.ClientSession`
        Your application's aiohttp client session.
        See http://aiohttp.readthedocs.io/en/stable/client.html.
    github_api_token : `str`
        A GitHub personal API token. See the `GitHub personal access token
        guide`_.
    ltd_product_url : `str`
        URL of the technote's product resource in the LTD Keeper API.
    mongo_collection : `motor.motor_asyncio.AsyncIOMotorCollection`, optional
        MongoDB collection. This should be the common MongoDB collection for
        LSST projectmeta JSON-LD records. If provided, ths JSON-LD is upserted
        into the MongoDB collection.

    Returns
    -------
    metadata : `dict`
        JSON-LD-formatted dictionary.

    .. `GitHub personal access token guide`: https://ls.st/41d
    """
    logger = logging.getLogger(__name__)

    ltd_product_data = await get_ltd_product(session, url=ltd_product_url)

    # Ensure the LTD product is a document
    product_name = ltd_product_data['slug']
    doc_handle_match = DOCUMENT_HANDLE_PATTERN.match(product_name)
    if doc_handle_match is None:
        logger.debug('%s is not a document repo', product_name)
        return

    # Figure out the format of the document by probing for metadata files.
    # reStructuredText-based Sphinx documents have metadata.yaml file.
    try:
        return await process_sphinx_technote(session,
                                             github_api_token,
                                             ltd_product_data,
                                             mongo_collection=mongo_collection)
    except NotSphinxTechnoteError:
        # Catch error so we can try the next format
        logger.debug('%s is not a Sphinx-based technote.', product_name)
    except Exception:
        # Something bad happened trying to process the technote.
        # Log and just move on.
        logger.exception('Unexpected error trying to process %s', product_name)
        return

    # Try interpreting it as a Lander page with a /metadata.jsonld document
    try:
        return await process_lander_page(session,
                                         github_api_token,
                                         ltd_product_data,
                                         mongo_collection=mongo_collection)
    except NotLanderPageError:
        # Catch error so we can try the next format
        logger.debug('%s is not a Lander page with a metadata.jsonld file.',
                     product_name)
    except Exception:
        # Something bad happened; log and move on
        logger.exception('Unexpected error trying to process %s', product_name)
        return