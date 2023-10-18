def build(self, force=False):
        "Create the image gallery"

        if not self.albums:
            self.logger.warning("No albums found.")
            return

        def log_func(x):
            # 63 is the total length of progressbar, label, percentage, etc
            available_length = get_terminal_size()[0] - 64
            if x and available_length > 10:
                return x.name[:available_length]
            else:
                return ""

        try:
            with progressbar(self.albums.values(), label="Collecting files",
                             item_show_func=log_func, show_eta=False,
                             file=self.progressbar_target) as albums:
                media_list = [f for album in albums
                              for f in self.process_dir(album, force=force)]
        except KeyboardInterrupt:
            sys.exit('Interrupted')

        bar_opt = {'label': "Processing files",
                   'show_pos': True,
                   'file': self.progressbar_target}
        failed_files = []

        if self.pool:
            try:
                with progressbar(length=len(media_list), **bar_opt) as bar:
                    for res in self.pool.imap_unordered(worker, media_list):
                        if res:
                            failed_files.append(res)
                        bar.update(1)
                self.pool.close()
                self.pool.join()
            except KeyboardInterrupt:
                self.pool.terminate()
                sys.exit('Interrupted')
            except pickle.PicklingError:
                self.logger.critical(
                    "Failed to process files with the multiprocessing feature."
                    " This can be caused by some module import or object "
                    "defined in the settings file, which can't be serialized.",
                    exc_info=True)
                sys.exit('Abort')
        else:
            with progressbar(media_list, **bar_opt) as medias:
                for media_item in medias:
                    res = process_file(media_item)
                    if res:
                        failed_files.append(res)

        if failed_files:
            self.remove_files(failed_files)

        if self.settings['write_html']:
            album_writer = AlbumPageWriter(self.settings,
                                           index_title=self.title)
            album_list_writer = AlbumListPageWriter(self.settings,
                                                    index_title=self.title)
            with progressbar(self.albums.values(),
                             label="%16s" % "Writing files",
                             item_show_func=log_func, show_eta=False,
                             file=self.progressbar_target) as albums:
                for album in albums:
                    if album.albums:
                        if album.medias:
                            self.logger.warning(
                                "Album %s contains sub-albums and images. "
                                "Please move images to their own sub-album. "
                                "Images in album %s will not be visible.",
                                album.title, album.title
                            )
                        album_list_writer.write(album)
                    else:
                        album_writer.write(album)
        print('')

        signals.gallery_build.send(self)