def _handleRenderResult(self, request, result):
        """
        Handle the result from `IResource.render`.

        If the result is a `Deferred` then return `NOT_DONE_YET` and add
        a callback to write the result to the request when it arrives.
        """
        def _requestFinished(result, cancel):
            cancel()
            return result

        if not isinstance(result, Deferred):
            result = succeed(result)

        def _whenDone(result):
            render = getattr(result, 'render', lambda request: result)
            renderResult = render(request)
            if renderResult != NOT_DONE_YET:
                request.write(renderResult)
                request.finish()
            return result
        request.notifyFinish().addBoth(_requestFinished, result.cancel)
        result.addCallback(self._adaptToResource)
        result.addCallback(_whenDone)
        result.addErrback(request.processingFailed)
        return NOT_DONE_YET