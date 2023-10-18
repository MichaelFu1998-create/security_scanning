def catch_error(response):
        '''
        Checks for Errors in a Response.
        401 or 403 - Security Rules Violation.
        404 or 417 - Firebase NOT Found.
        response - (Request.Response) - response from a request.
        '''
        status = response.status_code
        if status == 401 or status == 403:
            raise EnvironmentError("Forbidden")
        elif status == 417 or status == 404:
            raise EnvironmentError("NotFound")