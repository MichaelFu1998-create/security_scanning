def create_coveragestore(self, name, workspace=None, path=None, type='GeoTIFF',
                             create_layer=True, layer_name=None, source_name=None, upload_data=False, contet_type="image/tiff"):
        """
        Create a coveragestore for locally hosted rasters.
        If create_layer is set to true, will create a coverage/layer.
        layer_name and source_name are only used if create_layer ia enabled. If not specified, the raster name will be used for both.
        """
        if path is None:
            raise Exception('You must provide a full path to the raster')

        if layer_name is not None and ":" in layer_name:
            ws_name, layer_name = layer_name.split(':')

        allowed_types = [
            'ImageMosaic',
            'GeoTIFF',
            'Gtopo30',
            'WorldImage',
            'AIG',
            'ArcGrid',
            'DTED',
            'EHdr',
            'ERDASImg',
            'ENVIHdr',
            'GeoPackage (mosaic)',
            'NITF',
            'RPFTOC',
            'RST',
            'VRT'
        ]

        if type is None:
            raise Exception('Type must be declared')
        elif type not in allowed_types:
            raise Exception('Type must be one of {}'.format(", ".join(allowed_types)))

        if workspace is None:
            workspace = self.get_default_workspace()
        workspace = _name(workspace)

        if upload_data is False:
            cs = UnsavedCoverageStore(self, name, workspace)
            cs.type = type
            cs.url = path if path.startswith("file:") else "file:{}".format(path)
            self.save(cs)

            if create_layer:
                if layer_name is None:
                    layer_name = os.path.splitext(os.path.basename(path))[0]
                if source_name is None:
                    source_name = os.path.splitext(os.path.basename(path))[0]

                data = "<coverage><name>{}</name><nativeName>{}</nativeName></coverage>".format(layer_name, source_name)
                url = "{}/workspaces/{}/coveragestores/{}/coverages.xml".format(self.service_url, workspace, name)
                headers = {"Content-type": "application/xml"}

                resp = self.http_request(url, method='post', data=data, headers=headers)
                if resp.status_code != 201:
                    FailedRequestError('Failed to create coverage/layer {} for : {}, {}'.format(layer_name, name,
                                                                                                resp.status_code, resp.text))
                self._cache.clear()
                return self.get_resources(names=layer_name, workspaces=workspace)[0]
        else:
            data = open(path, 'rb')
            params = {"configure": "first", "coverageName": name}
            url = build_url(
                self.service_url,
                [
                    "workspaces",
                    workspace,
                    "coveragestores",
                    name,
                    "file.{}".format(type.lower())
                ],
                params
            )

            headers = {"Content-type": contet_type}
            resp = self.http_request(url, method='put', data=data, headers=headers)

            if hasattr(data, "close"):
                data.close()

            if resp.status_code != 201:
                FailedRequestError('Failed to create coverage/layer {} for : {}, {}'.format(layer_name, name, resp.status_code, resp.text))

        return self.get_stores(names=name, workspaces=workspace)[0]