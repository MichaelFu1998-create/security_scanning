def update_links_and_ffts(self):
        """FFT (856) Dealing with graphs."""
        figure_counter = 0
        for field in record_get_field_instances(self.record,
                                                tag='856',
                                                ind1='4'):
            subs = field_get_subfields(field)

            newsubs = []
            remove = False

            if 'z' in subs:
                is_figure = [s for s in subs['z'] if "figure" in s.lower()]
                if is_figure and 'u' in subs:
                    is_subformat = [
                        s for s in subs['u'] if "subformat" in s.lower()]
                    if not is_subformat:
                        url = subs['u'][0]
                        if url.endswith(".pdf"):
                            # We try to convert
                            fd, local_url = mkstemp(suffix=os.path.basename(url))
                            os.close(fd)
                            self.logger.info(
                                "Downloading %s into %s" % (url, local_url))
                            plotfile = ""
                            try:
                                plotfile = download_file(url=url,
                                                         download_to_file=local_url)
                            except Exception as e:
                                self.logger.exception(e)
                                remove = True
                            if plotfile:
                                converted = convert_images([plotfile])
                                if converted:
                                    url = converted.pop()
                                    msg = "Successfully converted %s to %s" \
                                          % (local_url, url)
                                    self.logger.info(msg)
                                else:
                                    msg = "Conversion failed on %s" \
                                          % (local_url,)
                                    self.logger.error(msg)
                                    url = None
                                    remove = True
                        if url:
                            newsubs.append(('a', url))
                            newsubs.append(('t', 'Plot'))
                            figure_counter += 1
                            if 'y' in subs:
                                newsubs.append(
                                    ('d', "%05d %s" % (figure_counter, subs['y'][0])))
                                newsubs.append(('n', subs['y'][0]))
                            else:
                                # Get basename without extension.
                                name = os.path.basename(
                                    os.path.splitext(subs['u'][0])[0])
                                newsubs.append(
                                    ('d', "%05d %s" % (figure_counter, name)))
                                newsubs.append(('n', name))

            if not newsubs and 'u' in subs:
                is_fulltext = [s for s in subs['u'] if ".pdf" in s]
                if is_fulltext:
                    newsubs = [('t', 'INSPIRE-PUBLIC'), ('a', subs['u'][0])]

            if not newsubs and 'u' in subs:
                remove = True
                is_zipfile = [s for s in subs['u'] if ".zip" in s]
                if is_zipfile:
                    url = is_zipfile[0]

                    local_url = os.path.join(self.get_local_folder(), os.path.basename(url))
                    self.logger.info("Downloading %s into %s" %
                                     (url, local_url))
                    zipped_archive = ""
                    try:
                        zipped_archive = download_file(url=is_zipfile[0],
                                                      download_to_file=local_url)
                    except Exception as e:
                        self.logger.exception(e)
                        remove = True
                    if zipped_archive:
                        unzipped_archive = unzip(zipped_archive)
                        list_of_pngs = locate("*.png", unzipped_archive)
                        for png in list_of_pngs:
                            if "_vti_" in png or "__MACOSX" in png:
                                continue
                            figure_counter += 1
                            plotsubs = []
                            plotsubs.append(('a', png))
                            caption = '%05d %s' % (
                                figure_counter, os.path.basename(png))
                            plotsubs.append(('d', caption))
                            plotsubs.append(('t', 'Plot'))
                            record_add_field(
                                self.record, 'FFT', subfields=plotsubs)

            if not remove and not newsubs and 'u' in subs:
                urls = ('http://cdsweb.cern.ch', 'http://cms.cern.ch',
                        'http://cmsdoc.cern.ch', 'http://documents.cern.ch',
                        'http://preprints.cern.ch', 'http://cds.cern.ch')
                for val in subs['u']:
                    if any(url in val for url in urls):
                        remove = True
                        break
                    if val.endswith('ps.gz'):
                        remove = True

            if newsubs:
                record_add_field(self.record, 'FFT', subfields=newsubs)
                remove = True

            if remove:
                record_delete_field(self.record, '856', ind1='4',
                                    field_position_global=field[4])