def get_chip(self, coordinates, catid, chip_type='PAN', chip_format='TIF', filename='chip.tif'):
        """Downloads a native resolution, orthorectified chip in tif format
        from a user-specified catalog id.

        Args:
            coordinates (list): Rectangle coordinates in order West, South, East, North.
                                West and East are longitudes, North and South are latitudes.
                                The maximum chip size is (2048 pix)x(2048 pix)
            catid (str): The image catalog id.
            chip_type (str): 'PAN' (panchromatic), 'MS' (multispectral), 'PS' (pansharpened).
                             'MS' is 4 or 8 bands depending on sensor.
            chip_format (str): 'TIF' or 'PNG'
            filename (str): Where to save chip.

        Returns:
            True if chip is successfully downloaded; else False.
        """

        def t2s1(t):
            # Tuple to string 1
            return str(t).strip('(,)').replace(',', '')

        def t2s2(t):
            # Tuple to string 2
            return str(t).strip('(,)').replace(' ', '')

        if len(coordinates) != 4:
            print('Wrong coordinate entry')
            return False

        W, S, E, N = coordinates
        box = ((W, S), (W, N), (E, N), (E, S), (W, S))
        box_wkt = 'POLYGON ((' + ','.join([t2s1(corner) for corner in box]) + '))'

        # get IDAHO images which intersect box
        results = self.get_images_by_catid_and_aoi(catid=catid, aoi_wkt=box_wkt)
        description = self.describe_images(results)

        pan_id, ms_id, num_bands = None, None, 0
        for catid, images in description.items():
            for partnum, part in images['parts'].items():
                if 'PAN' in part.keys():
                    pan_id = part['PAN']['id']
                    bucket = part['PAN']['bucket']
                if 'WORLDVIEW_8_BAND' in part.keys():
                    ms_id = part['WORLDVIEW_8_BAND']['id']
                    num_bands = 8
                    bucket = part['WORLDVIEW_8_BAND']['bucket']
                elif 'RGBN' in part.keys():
                    ms_id = part['RGBN']['id']
                    num_bands = 4
                    bucket = part['RGBN']['bucket']

        # specify band information
        band_str = ''
        if chip_type == 'PAN':
            band_str = pan_id + '?bands=0'
        elif chip_type == 'MS':
            band_str = ms_id + '?'
        elif chip_type == 'PS':
            if num_bands == 8:
                band_str = ms_id + '?bands=4,2,1&panId=' + pan_id
            elif num_bands == 4:
                band_str = ms_id + '?bands=0,1,2&panId=' + pan_id

        # specify location information
        location_str = '&upperLeft={}&lowerRight={}'.format(t2s2((W, N)), t2s2((E, S)))

        service_url = 'https://idaho.geobigdata.io/v1/chip/bbox/' + bucket + '/'
        url = service_url + band_str + location_str
        url += '&format=' + chip_format + '&token=' + self.gbdx_connection.access_token
        r = requests.get(url)

        if r.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(r.content)
                return True
        else:
            print('Cannot download chip')
            return False