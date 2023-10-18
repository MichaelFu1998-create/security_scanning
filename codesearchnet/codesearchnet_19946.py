def _record_info(self, setup_info=None):
        """
        All launchers should call this method to write the info file
        at the end of the launch. The .info file is saved given
        setup_info supplied by _setup_launch into the
        root_directory. When called without setup_info, the existing
        info file is updated with the end-time.
        """
        info_path = os.path.join(self.root_directory, ('%s.info' % self.batch_name))

        if setup_info is None:
            try:
                with open(info_path, 'r') as info_file:
                    setup_info = json.load(info_file)
            except:
                setup_info = {}

            setup_info.update({'end_time' : tuple(time.localtime())})
        else:
            setup_info.update({
                'end_time' : None,
                'metadata' : self.metadata
                })

        with open(info_path, 'w') as info_file:
            json.dump(setup_info, info_file, sort_keys=True, indent=4)