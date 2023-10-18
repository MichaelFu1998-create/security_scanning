def histogram_match(self, use_bands, blm_source=None, **kwargs):
        ''' Match the histogram to existing imagery '''
        assert has_rio, "To match image histograms please install rio_hist"
        data = self._read(self[use_bands,...], **kwargs)
        data = np.rollaxis(data.astype(np.float32), 0, 3)
        if 0 in data:
            data = np.ma.masked_values(data, 0)
        bounds = self._reproject(box(*self.bounds), from_proj=self.proj, to_proj="EPSG:4326").bounds
        if blm_source == 'browse':
            from gbdxtools.images.browse_image import BrowseImage
            ref = BrowseImage(self.cat_id, bbox=bounds).read()
        else:
            from gbdxtools.images.tms_image import TmsImage
            tms = TmsImage(zoom=self._calc_tms_zoom(self.affine[0]), bbox=bounds, **kwargs)
            ref = np.rollaxis(tms.read(), 0, 3)
        out = np.dstack([rio_match(data[:,:,idx], ref[:,:,idx].astype(np.double)/255.0)
                        for idx in range(data.shape[-1])])
        if 'stretch' in kwargs or 'gamma' in kwargs:
            return self._histogram_stretch(out, **kwargs)
        else:
            return out