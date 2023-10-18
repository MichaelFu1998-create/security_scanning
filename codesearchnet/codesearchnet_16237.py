def detail_view(self, request, module, preview):
        """
        Looks up a preview in the index, returning a detail view response.
        """
        try:
            preview = self.__previews[module][preview]
        except KeyError:
            raise Http404  # The provided module/preview does not exist in the index.
        return preview.detail_view(request)