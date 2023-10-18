async def get_response(self, path: str, scope: Scope) -> Response:
        """
        Returns an HTTP response, given the incoming path, method and request headers.
        """
        if scope["method"] not in ("GET", "HEAD"):
            return PlainTextResponse("Method Not Allowed", status_code=405)

        if path.startswith(".."):
            # Most clients will normalize the path, so we shouldn't normally
            # get this, but don't allow misbehaving clients to break out of
            # the static files directory.
            return PlainTextResponse("Not Found", status_code=404)

        full_path, stat_result = await self.lookup_path(path)

        if stat_result and stat.S_ISREG(stat_result.st_mode):
            # We have a static file to serve.
            return self.file_response(full_path, stat_result, scope)

        elif stat_result and stat.S_ISDIR(stat_result.st_mode) and self.html:
            # We're in HTML mode, and have got a directory URL.
            # Check if we have 'index.html' file to serve.
            index_path = os.path.join(path, "index.html")
            full_path, stat_result = await self.lookup_path(index_path)
            if stat_result is not None and stat.S_ISREG(stat_result.st_mode):
                if not scope["path"].endswith("/"):
                    # Directory URLs should redirect to always end in "/".
                    url = URL(scope=scope)
                    url = url.replace(path=url.path + "/")
                    return RedirectResponse(url=url)
                return self.file_response(full_path, stat_result, scope)

        if self.html:
            # Check for '404.html' if we're in HTML mode.
            full_path, stat_result = await self.lookup_path("404.html")
            if stat_result is not None and stat.S_ISREG(stat_result.st_mode):
                return self.file_response(
                    full_path, stat_result, scope, status_code=404
                )

        return PlainTextResponse("Not Found", status_code=404)