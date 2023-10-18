def _adaptToResource(self, result):
        """
        Adapt a result to `IResource`.

        Several adaptions are tried they are, in order: ``None``,
        `IRenderable <twisted:twisted.web.iweb.IRenderable>`, `IResource
        <twisted:twisted.web.resource.IResource>`, and `URLPath
        <twisted:twisted.python.urlpath.URLPath>`. Anything else is returned as
        is.

        A `URLPath <twisted:twisted.python.urlpath.URLPath>` is treated as
        a redirect.
        """
        if result is None:
            return NotFound()

        spinneretResource = ISpinneretResource(result, None)
        if spinneretResource is not None:
            return SpinneretResource(spinneretResource)

        renderable = IRenderable(result, None)
        if renderable is not None:
            return _RenderableResource(renderable)

        resource = IResource(result, None)
        if resource is not None:
            return resource

        if isinstance(result, URLPath):
            return Redirect(str(result))

        return result