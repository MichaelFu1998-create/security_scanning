def get_publication_date(self, xml_doc):
        """Return the best effort start_date."""
        start_date = get_value_in_tag(xml_doc, "prism:coverDate")
        if not start_date:
            start_date = get_value_in_tag(xml_doc, "prism:coverDisplayDate")
            if not start_date:
                start_date = get_value_in_tag(xml_doc, 'oa:openAccessEffective')
                if start_date:
                    start_date = datetime.datetime.strptime(
                        start_date, "%Y-%m-%dT%H:%M:%SZ"
                    )
                    return start_date.strftime("%Y-%m-%d")
            import dateutil.parser
            #dateutil.parser.parse cant process dates like April-June 2016
            start_date = re.sub('([A-Z][a-z]+)[\s\-][A-Z][a-z]+ (\d{4})', 
                                r'\1 \2', start_date)
            try:
                date = dateutil.parser.parse(start_date)
            except ValueError:
                return ''
            # Special case where we ignore the deduced day form dateutil
            # in case it was not given in the first place.
            if len(start_date.split(" ")) == 3:
                return date.strftime("%Y-%m-%d")
            else:
                return date.strftime("%Y-%m")
        else:
            if len(start_date) is 8:
                start_date = time.strftime(
                    '%Y-%m-%d', time.strptime(start_date, '%Y%m%d'))
            elif len(start_date) is 6:
                start_date = time.strftime(
                    '%Y-%m', time.strptime(start_date, '%Y%m'))
            return start_date