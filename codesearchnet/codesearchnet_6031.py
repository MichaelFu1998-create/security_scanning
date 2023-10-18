def publish_featuretype(self, name, store, native_crs, srs=None, jdbc_virtual_table=None, native_name=None):
        '''Publish a featuretype from data in an existing store'''
        # @todo native_srs doesn't seem to get detected, even when in the DB
        # metadata (at least for postgis in geometry_columns) and then there
        # will be a misconfigured layer
        if native_crs is None:
            raise ValueError("must specify native_crs")

        srs = srs or native_crs
        feature_type = FeatureType(self, store.workspace, store, name)
        # because name is the in FeatureType base class, work around that
        # and hack in these others that don't have xml properties
        feature_type.dirty['name'] = name
        feature_type.dirty['srs'] = srs
        feature_type.dirty['nativeCRS'] = native_crs
        feature_type.enabled = True
        feature_type.advertised = True
        feature_type.title = name

        if native_name is not None:
            feature_type.native_name = native_name

        headers = {
            "Content-type": "application/xml",
            "Accept": "application/xml"
        }

        resource_url = store.resource_url
        if jdbc_virtual_table is not None:
            feature_type.metadata = ({'JDBC_VIRTUAL_TABLE': jdbc_virtual_table})
            params = dict()
            resource_url = build_url(
                self.service_url,
                [
                    "workspaces",
                    store.workspace.name,
                    "datastores", store.name,
                    "featuretypes.xml"
                ],
                params
            )

        resp = self.http_request(resource_url, method='post', data=feature_type.message(), headers=headers)
        if resp.status_code not in (200, 201, 202):
            FailedRequestError('Failed to publish feature type {} : {}, {}'.format(name, resp.status_code, resp.text))

        self._cache.clear()
        feature_type.fetch()
        return feature_type