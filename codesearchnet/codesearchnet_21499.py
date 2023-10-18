async def _upload_to_mongodb(collection, jsonld):
    """Upsert the technote resource into the projectmeta MongoDB collection.

    Parameters
    ----------
    collection : `motor.motor_asyncio.AsyncIOMotorCollection`
        The MongoDB collection.
    jsonld : `dict`
        The JSON-LD document that represents the document resource.
    """
    document = {
        'data': jsonld
    }
    query = {
        'data.reportNumber': jsonld['reportNumber']
    }
    await collection.update(query, document, upsert=True, multi=False)