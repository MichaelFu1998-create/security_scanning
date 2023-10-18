def elastic_query(model, query, session=None, enabled_fields=None):
    """ Public method for init the class ElasticQuery
        :model: SQLAlchemy model
        :query: valid string like a ElasticSearch
        :session: SQLAlchemy session *optional
        :enabled_fields: Fields allowed for make a query *optional
    """
    # TODO: make session to optional
    instance = ElasticQuery(model, query, session, enabled_fields)
    return instance.search()