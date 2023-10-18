def _issue_cert(self, domain):
        """
        Issue a certificate for the given domain.
        """
        def errback(failure):
            # Don't fail on some of the errors we could get from the ACME
            # server, rather just log an error so that we can continue with
            # other domains.
            failure.trap(txacme_ServerError)
            acme_error = failure.value.message

            if acme_error.code in ['rateLimited', 'serverInternal',
                                   'connection', 'unknownHost']:
                # TODO: Fire off an error to Sentry or something?
                self.log.error(
                    'Error ({code}) issuing certificate for "{domain}": '
                    '{detail}', code=acme_error.code, domain=domain,
                    detail=acme_error.detail)
            else:
                # There are more error codes but if they happen then something
                # serious has gone wrong-- carry on error-ing.
                return failure

        d = self.txacme_service.issue_cert(domain)
        return d.addErrback(errback)