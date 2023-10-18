def main():
    """Command line entrypoint to reduce technote metadata.
    """
    parser = argparse.ArgumentParser(
        description='Discover and ingest metadata from document sources, '
                    'including lsstdoc-based LaTeX documents and '
                    'reStructuredText-based technotes. Metadata can be '
                    'upserted into the LSST Projectmeta MongoDB.')
    parser.add_argument(
        '--ltd-product',
        dest='ltd_product_url',
        help='URL of an LSST the Docs product '
             '(https://keeper.lsst.codes/products/<slug>). If provided, '
             'only this document will be ingested.')
    parser.add_argument(
        '--github-token',
        help='GitHub personal access token.')
    parser.add_argument(
        '--mongodb-uri',
        help='MongoDB connection URI. If provided, metadata will be loaded '
             'into the Projectmeta database. Omit this argument to just '
             'test the ingest pipeline.')
    parser.add_argument(
        '--mongodb-db',
        default='lsstprojectmeta',
        help='Name of MongoDB database')
    parser.add_argument(
        '--mongodb-collection',
        default='resources',
        help='Name of the MongoDB collection for projectmeta resources')
    args = parser.parse_args()

    # Configure the root logger
    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter(
        '%(asctime)s %(levelname)8s %(name)s | %(message)s')
    stream_handler.setFormatter(stream_formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(stream_handler)
    root_logger.setLevel(logging.WARNING)
    # Configure app logger
    app_logger = logging.getLogger('lsstprojectmeta')
    app_logger.setLevel(logging.DEBUG)

    if args.mongodb_uri is not None:
        mongo_client = AsyncIOMotorClient(args.mongodb_uri, ssl=True)
        collection = mongo_client[args.mongodb_db][args.mongodb_collection]
    else:
        collection = None

    loop = asyncio.get_event_loop()

    if args.ltd_product_url is not None:
        # Run single technote
        loop.run_until_complete(run_single_ltd_doc(args.ltd_product_url,
                                                   args.github_token,
                                                   collection))
    else:
        # Run bulk technote processing
        loop.run_until_complete(run_bulk_etl(args.github_token,
                                             collection))