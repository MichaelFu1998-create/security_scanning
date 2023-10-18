def get_tms_layers(self,
                       catid,
                       bands='4,2,1',
                       gamma=1.3,
                       highcutoff=0.98,
                       lowcutoff=0.02,
                       brightness=1.0,
                       contrast=1.0):
        """Get list of urls and bounding boxes corrsponding to idaho images for a given catalog id.

        Args:
           catid (str): Catalog id
           bands (str): Bands to display, separated by commas (0-7).
           gamma (float): gamma coefficient. This is for on-the-fly pansharpening.
           highcutoff (float): High cut off coefficient (0.0 to 1.0). This is for on-the-fly pansharpening.
           lowcutoff (float): Low cut off coefficient (0.0 to 1.0). This is for on-the-fly pansharpening.
           brightness (float): Brightness coefficient (0.0 to 1.0). This is for on-the-fly pansharpening.
           contrast (float): Contrast coefficient (0.0 to 1.0). This is for on-the-fly pansharpening.

        Returns:
           urls (list): TMS urls.
           bboxes (list of tuples): Each tuple is (W, S, E, N) where (W,S,E,N) are the bounds of the corresponding idaho part.
        """

        description = self.describe_images(self.get_images_by_catid(catid))
        service_url = 'http://idaho.geobigdata.io/v1/tile/'

        urls, bboxes = [], []
        for catid, images in description.items():
            for partnum, part in images['parts'].items():
                if 'PAN' in part.keys():
                    pan_id = part['PAN']['id']
                if 'WORLDVIEW_8_BAND' in part.keys():
                    ms_id = part['WORLDVIEW_8_BAND']['id']
                    ms_partname = 'WORLDVIEW_8_BAND'
                elif 'RGBN' in part.keys():
                    ms_id = part['RGBN']['id']
                    ms_partname = 'RGBN'

                if ms_id:
                    if pan_id:
                        band_str = ms_id + '/{z}/{x}/{y}?bands=' + bands + '&panId=' + pan_id
                    else:
                        band_str = ms_id + '/{z}/{x}/{y}?bands=' + bands
                    bbox = from_wkt(part[ms_partname]['boundstr']).bounds
                elif not ms_id and pan_id:
                    band_str = pan_id + '/{z}/{x}/{y}?bands=0'
                    bbox = from_wkt(part['PAN']['boundstr']).bounds
                else:
                    continue

                bboxes.append(bbox)

                # Get the bucket. It has to be the same for all entries in the part.
                bucket = part[list(part.keys())[0]]['bucket']

                # Get the token
                token = self.gbdx_connection.access_token

                # Assemble url
                url = (service_url + bucket + '/'
                       + band_str
                       + """&gamma={}
                                        &highCutoff={}
                                        &lowCutoff={}
                                        &brightness={}
                                        &contrast={}
                                        &token={}""".format(gamma,
                                                            highcutoff,
                                                            lowcutoff,
                                                            brightness,
                                                            contrast,
                                                            token))
                urls.append(url)

        return urls, bboxes