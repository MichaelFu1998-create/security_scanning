def get_request_date(cls, req):
        """
        Try to pull a date from the request by looking first at the
        x-amz-date header, and if that's not present then the Date header.

        Return a datetime.date object, or None if neither date header
        is found or is in a recognisable format.

        req -- a requests PreparedRequest object

        """
        date = None
        for header in ['x-amz-date', 'date']:
            if header not in req.headers:
                continue
            try:
                date_str = cls.parse_date(req.headers[header])
            except DateFormatError:
                continue
            try:
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                continue
            else:
                break

        return date