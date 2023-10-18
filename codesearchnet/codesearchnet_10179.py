def pif_multi_search(self, multi_query):
        """
        Run each in a list of PIF queries against Citrination.

        :param multi_query: :class:`MultiQuery` object to execute.
        :return: :class:`PifMultiSearchResult` object with the results of the query.
        """
        failure_message = "Error while making PIF multi search request"
        response_dict = self._get_success_json(
            self._post(routes.pif_multi_search, data=json.dumps(multi_query, cls=QueryEncoder),
                       failure_message=failure_message))

        return PifMultiSearchResult(**keys_to_snake_case(response_dict['results']))