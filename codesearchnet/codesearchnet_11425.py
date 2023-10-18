def search(self,
               query_string=None,
               field_dictionary=None,
               filter_dictionary=None,
               exclude_dictionary=None,
               facet_terms=None,
               exclude_ids=None,
               use_field_match=False,
               **kwargs):  # pylint: disable=too-many-arguments, too-many-locals, too-many-branches, arguments-differ
        """
        Implements call to search the index for the desired content.

        Args:
            query_string (str): the string of values upon which to search within the
            content of the objects within the index

            field_dictionary (dict): dictionary of values which _must_ exist and
            _must_ match in order for the documents to be included in the results

            filter_dictionary (dict): dictionary of values which _must_ match if the
            field exists in order for the documents to be included in the results;
            documents for which the field does not exist may be included in the
            results if they are not otherwise filtered out

            exclude_dictionary(dict): dictionary of values all of which which must
            not match in order for the documents to be included in the results;
            documents which have any of these fields and for which the value matches
            one of the specified values shall be filtered out of the result set

            facet_terms (dict): dictionary of terms to include within search
            facets list - key is the term desired to facet upon, and the value is a
            dictionary of extended information to include. Supported right now is a
            size specification for a cap upon how many facet results to return (can
            be an empty dictionary to use default size for underlying engine):

            e.g.
            {
                "org": {"size": 10},  # only show top 10 organizations
                "modes": {}
            }

            use_field_match (bool): flag to indicate whether to use elastic
            filtering or elastic matching for field matches - this is nothing but a
            potential performance tune for certain queries

            (deprecated) exclude_ids (list): list of id values to exclude from the results -
            useful for finding maches that aren't "one of these"

        Returns:
            dict object with results in the desired format
            {
                "took": 3,
                "total": 4,
                "max_score": 2.0123,
                "results": [
                    {
                        "score": 2.0123,
                        "data": {
                            ...
                        }
                    },
                    {
                        "score": 0.0983,
                        "data": {
                            ...
                        }
                    }
                ],
                "facets": {
                    "org": {
                        "total": total_count,
                        "other": 1,
                        "terms": {
                            "MITx": 25,
                            "HarvardX": 18
                        }
                    },
                    "modes": {
                        "total": modes_count,
                        "other": 15,
                        "terms": {
                            "honor": 58,
                            "verified": 44,
                        }
                    }
                }
            }

        Raises:
            ElasticsearchException when there is a problem with the response from elasticsearch

        Example usage:
            .search(
                "find the words within this string",
                {
                    "must_have_field": "mast_have_value for must_have_field"
                },
                {

                }
            )
        """

        log.debug("searching index with %s", query_string)

        elastic_queries = []
        elastic_filters = []

        # We have a query string, search all fields for matching text within the "content" node
        if query_string:
            if six.PY2:
                query_string = query_string.encode('utf-8').translate(None, RESERVED_CHARACTERS)
            else:
                query_string = query_string.translate(query_string.maketrans('', '', RESERVED_CHARACTERS))
            elastic_queries.append({
                "query_string": {
                    "fields": ["content.*"],
                    "query": query_string
                }
            })

        if field_dictionary:
            if use_field_match:
                elastic_queries.extend(_process_field_queries(field_dictionary))
            else:
                elastic_filters.extend(_process_field_filters(field_dictionary))

        if filter_dictionary:
            elastic_filters.extend(_process_filters(filter_dictionary))

        # Support deprecated argument of exclude_ids
        if exclude_ids:
            if not exclude_dictionary:
                exclude_dictionary = {}
            if "_id" not in exclude_dictionary:
                exclude_dictionary["_id"] = []
            exclude_dictionary["_id"].extend(exclude_ids)

        if exclude_dictionary:
            elastic_filters.append(_process_exclude_dictionary(exclude_dictionary))

        query_segment = {
            "match_all": {}
        }
        if elastic_queries:
            query_segment = {
                "bool": {
                    "must": elastic_queries
                }
            }

        query = query_segment
        if elastic_filters:
            filter_segment = {
                "bool": {
                    "must": elastic_filters
                }
            }
            query = {
                "filtered": {
                    "query": query_segment,
                    "filter": filter_segment,
                }
            }

        body = {"query": query}
        if facet_terms:
            facet_query = _process_facet_terms(facet_terms)
            if facet_query:
                body["facets"] = facet_query

        try:
            es_response = self._es.search(
                index=self.index_name,
                body=body,
                **kwargs
            )
        except exceptions.ElasticsearchException as ex:
            message = six.text_type(ex)
            if 'QueryParsingException' in message:
                log.exception("Malformed search query: %s", message)
                raise QueryParseError('Malformed search query.')
            else:
                # log information and re-raise
                log.exception("error while searching index - %s", str(message))
                raise

        return _translate_hits(es_response)