def build_jsonld(self, url=None, code_url=None, ci_url=None,
                     readme_url=None, license_id=None):
        """Create a JSON-LD representation of this LSST LaTeX document.

        Parameters
        ----------
        url : `str`, optional
            URL where this document is published to the web. Prefer
            the LSST the Docs URL if possible.
            Example: ``'https://ldm-151.lsst.io'``.
        code_url : `str`, optional
            Path the the document's repository, typically on GitHub.
            Example: ``'https://github.com/lsst/LDM-151'``.
        ci_url : `str`, optional
            Path to the continuous integration service dashboard for this
            document's repository.
            Example: ``'https://travis-ci.org/lsst/LDM-151'``.
        readme_url : `str`, optional
            URL to the document repository's README file. Example:
            ``https://raw.githubusercontent.com/lsst/LDM-151/master/README.rst``.
        license_id : `str`, optional
            License identifier, if known. The identifier should be from the
            listing at https://spdx.org/licenses/. Example: ``CC-BY-4.0``.

        Returns
        -------
        jsonld : `dict`
            JSON-LD-formatted dictionary.
        """
        jsonld = {
            '@context': [
                "https://raw.githubusercontent.com/codemeta/codemeta/2.0-rc/"
                "codemeta.jsonld",
                "http://schema.org"],
            '@type': ['Report', 'SoftwareSourceCode'],
            'language': 'TeX',
            'reportNumber': self.handle,
            'name': self.plain_title,
            'description': self.plain_abstract,
            'author': [{'@type': 'Person', 'name': author_name}
                       for author_name in self.plain_authors],
            # This is a datetime.datetime; not a string. If writing to a file,
            # Need to convert this to a ISO 8601 string.
            'dateModified': self.revision_datetime
        }

        try:
            jsonld['articleBody'] = self.plain_content
            jsonld['fileFormat'] = 'text/plain'  # MIME type of articleBody
        except RuntimeError:
            # raised by pypandoc when it can't convert the tex document
            self._logger.exception('Could not convert latex body to plain '
                                   'text for articleBody.')
            self._logger.warning('Falling back to tex source for articleBody')
            jsonld['articleBody'] = self._tex
            jsonld['fileFormat'] = 'text/plain'  # no mimetype for LaTeX?

        if url is not None:
            jsonld['@id'] = url
            jsonld['url'] = url
        else:
            # Fallback to using the document handle as the ID. This isn't
            # entirely ideal from a linked data perspective.
            jsonld['@id'] = self.handle

        if code_url is not None:
            jsonld['codeRepository'] = code_url

        if ci_url is not None:
            jsonld['contIntegration'] = ci_url

        if readme_url is not None:
            jsonld['readme'] = readme_url

        if license_id is not None:
            jsonld['license_id'] = None

        return jsonld