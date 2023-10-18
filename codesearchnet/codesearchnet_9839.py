def redirect(self, request):
        """Handle redirects properly."""
        url = request.path
        querystring = request.GET.copy()
        if self.logout_key and self.logout_key in request.GET:
            del querystring[self.logout_key]
        if querystring:
            url = '%s?%s' % (url, querystring.urlencode())
        return HttpResponseRedirect(url)