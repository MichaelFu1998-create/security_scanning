def _translate_hits(es_response):
    """ Provide resultset in our desired format from elasticsearch results """

    def translate_result(result):
        """ Any conversion from ES result syntax into our search engine syntax """
        translated_result = copy.copy(result)
        data = translated_result.pop("_source")

        translated_result.update({
            "data": data,
            "score": translated_result["_score"]
        })

        return translated_result

    def translate_facet(result):
        """ Any conversion from ES facet syntax into our search engine sytax """
        terms = {term["term"]: term["count"] for term in result["terms"]}
        return {
            "terms": terms,
            "total": result["total"],
            "other": result["other"],
        }

    results = [translate_result(hit) for hit in es_response["hits"]["hits"]]
    response = {
        "took": es_response["took"],
        "total": es_response["hits"]["total"],
        "max_score": es_response["hits"]["max_score"],
        "results": results,
    }

    if "facets" in es_response:
        response["facets"] = {facet: translate_facet(es_response["facets"][facet]) for facet in es_response["facets"]}

    return response