async def process_ltd_doc_products(session, product_urls, github_api_token,
                                   mongo_collection=None):
    """Run a pipeline to process extract, transform, and load metadata for
    multiple LSST the Docs-hosted projects

    Parameters
    ----------
    session : `aiohttp.ClientSession`
        Your application's aiohttp client session.
        See http://aiohttp.readthedocs.io/en/stable/client.html.
    product_urls : `list` of `str`
        List of LSST the Docs product URLs.
    github_api_token : `str`
        A GitHub personal API token. See the `GitHub personal access token
        guide`_.
    mongo_collection : `motor.motor_asyncio.AsyncIOMotorCollection`, optional
        MongoDB collection. This should be the common MongoDB collection for
        LSST projectmeta JSON-LD records.
    """
    tasks = [asyncio.ensure_future(
             process_ltd_doc(session, github_api_token,
                             product_url,
                             mongo_collection=mongo_collection))
             for product_url in product_urls]
    await asyncio.gather(*tasks)