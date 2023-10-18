def process_result(cls, dictionary, match_phrase, user):
        """
        Called from within search handler. Finds desired subclass and decides if the
        result should be removed and adds properties derived from the result information
        """
        result_processor = _load_class(getattr(settings, "SEARCH_RESULT_PROCESSOR", None), cls)
        srp = result_processor(dictionary, match_phrase)
        if srp.should_remove(user):
            return None
        try:
            srp.add_properties()
        # protect around any problems introduced by subclasses within their properties
        except Exception as ex:  # pylint: disable=broad-except
            log.exception("error processing properties for %s - %s: will remove from results",
                          json.dumps(dictionary, cls=DjangoJSONEncoder), str(ex))
            return None
        return dictionary