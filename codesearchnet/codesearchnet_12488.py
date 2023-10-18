def _histogram_stretch(self, data, **kwargs):
        ''' perform a contrast stretch and/or gamma adjustment '''
        limits = {}
        # get the image min-max statistics
        for x in range(3):
            band = data[:,:,x]
            try:
                limits[x] = np.percentile(band, kwargs.get("stretch", [0,100]))
            except IndexError:
                # this band has no dynamic range and cannot be stretched
                return data
        # compute the stretch
        for x in range(3):
            band = data[:,:,x]
            if 0 in band:
                band = np.ma.masked_values(band, 0).compressed()
            top = limits[x][1]
            bottom = limits[x][0]
            if top != bottom: # catch divide by zero
                data[:,:,x] = (data[:,:,x] - bottom) / float(top - bottom) * 255.0
        data = np.clip(data, 0, 255).astype("uint8")
        # gamma adjust
        if "gamma" in kwargs:
            invGamma = 1.0 / kwargs['gamma']
            lut = np.array([((i / 255.0) ** invGamma) * 255
		            for i in np.arange(0, 256)]).astype("uint8")
            data = np.take(lut, data)
        return data