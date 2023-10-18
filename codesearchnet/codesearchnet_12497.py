def create_leaflet_viewer(self, idaho_image_results, filename):
        """Create a leaflet viewer html file for viewing idaho images.

        Args:
            idaho_image_results (dict): IDAHO image result set as returned from
                                        the catalog.
            filename (str): Where to save output html file.
        """

        description = self.describe_images(idaho_image_results)
        if len(description) > 0:
            functionstring = ''
            for catid, images in description.items():
                for partnum, part in images['parts'].items():

                    num_images = len(list(part.keys()))
                    partname = None
                    if num_images == 1:
                        # there is only one image, use the PAN
                        partname = [p for p in list(part.keys())][0]
                        pan_image_id = ''
                    elif num_images == 2:
                        # there are two images in this part, use the multi (or pansharpen)
                        partname = [p for p in list(part.keys()) if p is not 'PAN'][0]
                        pan_image_id = part['PAN']['id']

                    if not partname:
                        self.logger.debug("Cannot find part for idaho image.")
                        continue

                    bandstr = {
                        'RGBN': '0,1,2',
                        'WORLDVIEW_8_BAND': '4,2,1',
                        'PAN': '0'
                    }.get(partname, '0,1,2')

                    part_boundstr_wkt = part[partname]['boundstr']
                    part_polygon = from_wkt(part_boundstr_wkt)
                    bucketname = part[partname]['bucket']
                    image_id = part[partname]['id']
                    W, S, E, N = part_polygon.bounds

                    functionstring += "addLayerToMap('%s','%s',%s,%s,%s,%s,'%s');\n" % (
                        bucketname, image_id, W, S, E, N, pan_image_id)

            __location__ = os.path.realpath(
                os.path.join(os.getcwd(), os.path.dirname(__file__)))
            try:
                with open(os.path.join(__location__, 'leafletmap_template.html'), 'r') as htmlfile:
                    data = htmlfile.read().decode("utf8")
            except AttributeError:
                with open(os.path.join(__location__, 'leafletmap_template.html'), 'r') as htmlfile:
                    data = htmlfile.read()

            data = data.replace('FUNCTIONSTRING', functionstring)
            data = data.replace('CENTERLAT', str(S))
            data = data.replace('CENTERLON', str(W))
            data = data.replace('BANDS', bandstr)
            data = data.replace('TOKEN', self.gbdx_connection.access_token)

            with codecs.open(filename, 'w', 'utf8') as outputfile:
                self.logger.debug("Saving %s" % filename)
                outputfile.write(data)
        else:
            print('No items returned.')