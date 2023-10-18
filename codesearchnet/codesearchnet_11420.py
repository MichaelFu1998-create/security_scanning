def log_indexing_error(cls, indexing_errors):
        """ Logs indexing errors and raises a general ElasticSearch Exception"""
        indexing_errors_log = []
        for indexing_error in indexing_errors:
            indexing_errors_log.append(str(indexing_error))
        raise exceptions.ElasticsearchException(', '.join(indexing_errors_log))